# Dockerfile for Lovable frontend
# This will be used once you add your Lovable code
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Expose port
EXPOSE 5173

# Development server (use nginx for production)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
