# Proyecto Cliente-Servidor

Prueba de docker-compose para conectar un client (React + Vite)
con un server (Pyhton) y con una bd (PostgreSQL) con interfaz grafica en pgadmin
Ademas de utilizar workers y Pub/Sub de GCP para las colas y la gestion de procesos

## Estructura principal del proyecto

- client/App.jsx: Pagina principal donde usar los diferentes componentes de client/pruebas/ para probar los diferentes servicios
- server/app.py: Diferentes endpoints para las pruebas
- db/init.sql: Sentencias SQL al iniciar el servicio

## Tecnologias usadas:

- Docker
- Python con Flask
- PostgreSQL con Pgadmin
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

### Pgadmin

Pqadmin es una UI que complementa al servicio de docker. Una vez esten especificados ambos servicios en docker-compose,
puedes abrir localhost:8080, meter las credenciales especificadas en el servicio de pgadmin e ingresar

Para poder ver cualquier tabla creada tienes que:

1. Click derecho sobre un server group (Servers por defecto)
2. Register > Server... y especificas todos los datos de las pestañas Genarl y Connections (host/name address es el nombre sel servicio de la db en docker)
3. Una vez este creado el server navegas hasta: Servers → Nombre → Databases → Nombre de la DB → Schemas → public → Tables
4. Con las tablas a la vista puedes ver todas sus caracteristicas y si haces click derecho > Vire/Edit data > All rows para ver todos los datos
