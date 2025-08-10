import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    /* 
      Creamos un Proxy para redirigir las peticiones a la API del servidor (Asi evitamos usar CORS)
      Esto es necesario porque el cliente corre en el puerto 5173 y el servidor en el 5000
      Cada vez que el cliente:5173 haga una petición a /api, vite redirige a el servidor:5000

      En caso de estar corriendo React+Vite en local se hace referencia a 'http://localhost:5000'
      Pero al correrlo desde Docker, el localhost es el propio contenedor (port 5173), por lo que no funciona
      Y hay que hacer referencia a 'http://server:5000', que es el nombre del servicio del servidor en docker-compose
    */
    proxy: {
      '/api': 'http://server:5000'
    }
  }
})
