FROM node:20-slim

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the default Vite port
EXPOSE 5173

# Run Vite development server, binding to all interfaces
CMD ["npm", "run", "dev", "--", "--host"]
