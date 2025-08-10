
# AVISO: Los workers no sirven para ejecutar tareas de DBs, sino para ejecutar tareas pesadas en segundo plano.
# En este caso se simula con una BD, pero no es su uso principal.


import time
import os
import psycopg2
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

# Configuración de conexión a la base de datos PostgreSQL desde variables de entorno
# Conexion_BBDD
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

# Pub/Sub settings
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

os.environ["PUBSUB_EMULATOR_HOST"] = os.getenv("PUBSUB_EMULATOR_HOST", "pubsub_emulator:8085")
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def update_task_status(task_id, video_url, status):
    """Inserta o actualiza el estado de la tarea en la base de datos."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Upsert para insertar o actualizar si existe
    cur.execute("""
        INSERT INTO video_tasks (task_id, video_url, status, created_at, updated_at)
        VALUES (%s, %s, %s, NOW(), NOW())
        ON CONFLICT (task_id) DO UPDATE
        SET status = EXCLUDED.status,
            updated_at = NOW();
    """, (task_id, video_url, status))
    conn.commit()
    cur.close()
    conn.close()

def process_video(task_id, video_url):
    print(f"[Worker] Procesando video {video_url} con ID {task_id}...")
    update_task_status(task_id, video_url, "Procesando")
    time.sleep(5)  # Simulación proceso pesado
    update_task_status(task_id, video_url, "Finalizado")
    print(f"[Worker] Video {task_id} procesado correctamente.")

def callback(message):
    data = message.data.decode("utf-8")
    print(f"[Worker] Mensaje recibido: {data}")
    message.ack()

    # Mensaje esperado: "task_id|video_url"
    try:
        task_id, video_url = data.split("|")
    except Exception as e:
        print(f"[Worker] Error al parsear el mensaje: {e}")
        return

    process_video(task_id, video_url)

def listen_for_messages():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"[Worker] Escuchando mensajes en {subscription_path}...\n")

    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    # Crear topic y subscripción si no existen
    try:
        publisher.create_topic(request={"name": topic_path})
        print("[Worker] Topic creado.")
    except Exception:
        print("[Worker] Topic ya existe.")

    try:
        subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        print("[Worker] Subscription creada.")
    except Exception:
        print("[Worker] Subscription ya existe.")

    listen_for_messages()
