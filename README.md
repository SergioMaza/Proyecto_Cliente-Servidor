# Proyecto Cliente-Servidor

Prueba de docker-compose para conectar un client (React + Vite)
con un server (Pyhton) y con una bd (PostgreSQL)
Ademas de utilizar workers y Pub/Sub de GCP para las colas y la gestion de procesos

## Tecnologias usadas:

- Docker
- Python con Flask
- PostgreSQL
- Google Pub/Sub en local (Colas)
- Workers (Procesos en segundo plano)

## Erroes típicos

- No tener corriendo docker desktops
- No habilitar el --host en: "dev": "vite --host"

## Aprendizajes

### Proxy

Para que los distintos servicios de docker se comuniquen correctamente entre ellos
hay que hacer en vite.config.js un proxy. Que servira como puente entre el cliente (port:5173)
y el server (port:5000), ya que sino, se bloquean las conexiones entre disitintos puertos.

En este caso el proxy intercepta todas las llamadas desde :5173/api/_
Y las transforma en :5000/api/_ para que el navegador no bloque la conexion.

Esto aplica en local, ya que si pasas a la nuve, los fetch serán a URL públicas.

### Funcionamiento de Workers y Pub/Sub

1. El cliente manda un vídeo a procesar → Flask publica un mensaje en Pub/Sub.
2. El worker recibe el mensaje, simula procesarlo y marca como “finalizado” en la db.
3. El cliente puede consultar el estado de las tareas a través de un endpoint /api/tasks/<id>.

#### Pasos

1. Crear worker/ con worker.py, el requirements.txt y el Dockerfile
2. Crear el servicio en docker-compose del worker y del emulador en local de Google Pub/Sub
3. Crear los endpoints necesarios en app.py
4. Crear la vista Workers_ProcesarVideo.jsx

