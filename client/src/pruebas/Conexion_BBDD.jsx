import { useEffect, useState } from "react";

export default function Conexion_BBDD() {
  const [usuarios, setUsuarios] = useState([]);
  const [mensaje, setMensaje] = useState("");

  // Función para cargar usuarios
  const cargarUsuarios = () => {
    fetch("/api/usuarios")
      .then((res) => res.json())
      .then((data) => setUsuarios(data))
      .catch(() => setMensaje("Error cargando usuarios"));
  };

  // Función para añadir usuario de ejemplo
  const añadirUsuario = () => {
    fetch("/api/add-user", { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        setMensaje(data.message);
        cargarUsuarios(); // Recarga la lista tras añadir
      })
      .catch(() => setMensaje("Error añadiendo usuario"));
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Usuarios</h2>
      <button onClick={añadirUsuario}>Añadir usuario de ejemplo</button>
      <p>{mensaje}</p>
      <ul>
        {usuarios.map((user, idx) => (
          <li key={idx}>{user.join(" - ")}</li>
        ))}
      </ul>
    </div>
  );
}
