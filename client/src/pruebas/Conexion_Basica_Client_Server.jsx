import React, { useState } from 'react'

export default function Conexion_Basica_Client_Server() {
  const [message, setMessage] = useState("Cargando...");
  
  /* Usado en proxy podemos hacer fech a /api con origen port:5173 y destino port:5000 */
  fetch("/api/ping")
    .then((res) => {
      console.log("Status:", res.status);
      if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
      return res.json();
    })
    .then((data) => {
      setMessage(data.message);
    })
    .catch((error) => {
      setMessage(`Error: ${error.message}`);
    });

  return (
    <div>
      <h1>Ping</h1>
      <p>{message}</p>
    </div>
  );
}


