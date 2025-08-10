import React, { useEffect, useState } from "react";

export default function ProcesarVideo() {
  const [videoUrl, setVideoUrl] = useState("");
  const [tasks, setTasks] = useState([]);

  // --- Función para obtener todas las tareas ---
  const fetchTasks = async () => {
    try {
      const res = await fetch("/api/tasks");
      const data = await res.json();
      setTasks(data);
    } catch (error) {
      console.error("Error obteniendo tareas:", error);
    }
  };

  // --- Función para obtener todas las tareas ---
  const deleteTasks = async () => {
    await fetch("/api/delete-all-tasks", { method: "POST" });
    fetchTasks();
  };

  // --- Refrescar la tabla cada 3 segundos ---
  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 1000);
    return () => clearInterval(interval);
  }, []);
  
  /* 
    Funcion asincrona para enviar el video al endpoint del server.
    El endpoint envia tareas a los workers via Pub/Sub
    y devuelve un ID de la tarea y su estado inicial.
  */
  const enviarVideo = async () => {
    await fetch("/api/process-video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_url: videoUrl }),
    });
    setVideoUrl("");
    fetchTasks();
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Procesar Video</h1>

      {/* Formulario para enviar video */}
      <input
        type="text"
        placeholder="URL del video"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        style={{ padding: "5px", marginRight: "10px", width: "300px" }}
      />
      <button onClick={enviarVideo}>Enviar</button>

      {/* Tabla de tareas */}
      <h2 style={{ marginTop: "20px" }}>Tareas en la base de datos</h2>
      <button onClick={deleteTasks}>Borrar todas las tareas</button>
      <table
        style={{
          borderCollapse: "collapse",
          width: "100%",
          border: "1px solid #ddd",
        }}
      >
        <thead>
          <tr style={{ background: "#212121ff" }}>
            <th style={thStyle}>Task ID</th>
            <th style={thStyle}>Video URL</th>
            <th style={thStyle}>Estado</th>
            <th style={thStyle}>Última actualización</th>
          </tr>
        </thead>
        <tbody>
          {tasks.length > 0 ? (
            tasks.map((task) => (
              <tr key={task.task_id}>
                <td style={tdStyle}>{task.task_id}</td>
                <td style={tdStyle}>{task.video_url}</td>
                <td style={tdStyle}>{task.status}</td>
                <td style={tdStyle}>
                  {task.updated_at
                    ? new Date(task.updated_at).toLocaleString()
                    : "-"}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td style={tdStyle} colSpan="4">
                No hay tareas registradas
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

// Estilos de tabla
const thStyle = {
  border: "1px solid #ddd",
  padding: "8px",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "8px",
};
