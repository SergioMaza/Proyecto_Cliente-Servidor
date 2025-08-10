# Imagen base de Node
FROM node:20

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos del package (dependencias)
COPY package*.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos todo el resto del código
COPY . .

# Exponemos el puerto que Vite usa por defecto
EXPOSE 5173

# Comando por defecto al iniciar el contenedor
CMD ["npm", "run", "dev"]