FROM node:20-slim

WORKDIR /app

# Copiamos los archivos de dependencias
COPY package*.json ./

# Instalamos las librerías
RUN npm install

# Copiamos el resto del código
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Comando para arrancar en modo desarrollo
CMD ["npm", "run", "dev", "--", "--host"]