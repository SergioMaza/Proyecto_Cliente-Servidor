from flask import Flask, jsonify, request

# BBDD
import psycopg2
import os

# Pub/Sub
from google.cloud import pubsub_v1
import uuid

app = Flask(__name__)

# Conexion_Basica_Client_Server
@app.route("/api/ping")
def ping():
    return jsonify({"message": "Pong"})
# ---

# Conexion_BBDD
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

@app.route("/api/usuarios")
def usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/add-user", methods=["POST"])
def add_user():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s);", ("Sergio", "sergio_ejemplos@gmail.com"))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Usuario añadido"})
    except Exception as e:
        print("Error en add_user:", e)
        return jsonify({"error": str(e)}), 500
# ---

# Pub/Sub
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

os.environ["PUBSUB_EMULATOR_HOST"] = os.getenv("PUBSUB_EMULATOR_HOST", "pubsub_emulator:8085")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

# Recibe un video_url y envía una tarea al worker via Pub/Sub.
@app.route("/api/process-video", methods=["POST"])
def process_video():
    # Obtiene y valida el video_url
    data = request.json
    video_url = data.get("video_url")
    if not video_url:
        return jsonify({"error": "Falta video_url"}), 400

    # Asigna un ID único a la tarea
    task_id = str(uuid.uuid4())

    # Publica el mensaje en el topic
    message = f"{task_id}|{video_url}"
    publisher.publish(topic_path, message.encode("utf-8"))

    return jsonify({"task_id": task_id, "status": "Pendiente"})
    
# Devuelve todas las tareas de la bd
@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT task_id, video_url, status, updated_at FROM video_tasks ORDER BY updated_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "task_id": row[0],
            "video_url": row[1],
            "status": row[2],
            "updated_at": row[3].isoformat() if row[3] else None
        })

    return jsonify(tasks)

# Borra todas las tareas de la bd
@app.route("/api/delete-all-tasks", methods=["POST"])
def delete_all_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM video_tasks")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Todas las tareas han sido borradas"})
# ---

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
