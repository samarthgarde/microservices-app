# Microservices App with Docker

This project demonstrates a simple microservices setup using **Frontend**, **Backend (Flask)**, **PostgreSQL database**, and **NGINX reverse proxy**, all running in Docker containers.

---

## Project Structure

```bash
microservices-app/
│
├── backend/
│ ├── app.py               # Flask backend app
│ ├── requirements.txt     # Python dependencies
│ └── Dockerfile           # Backend Dockerfile
│
├── frontend/
│ ├── index.html           # Frontend HTML
│ ├── favicon.ico
│ └── Dockerfile           # Frontend Dockerfile
│
├── nginx.conf             # NGINX reverse proxy configuration
└── README.md
```

---

## Docker Setup

### 1️⃣ Build Docker images

```bash
# Backend
cd backend
docker build -t flask-backend .

# Frontend
cd ../frontend
docker build -t html-frontend .
```
---

### 2️⃣ Run Containers

```bash
# Create network
docker network create app-network

# Database
docker run -d --name db --network app-network -e POSTGRES_DB=projectdb -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:15

# Backend
docker run -d --name backend --network app-network -p 5000:5000 flask-backend

# Frontend
docker run -d --name frontend --network app-network -p 8080:80 html-frontend

# NGINX Proxy
docker run -d --name proxy --network app-network -p 8081:80 -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx:alpine
```
---

### Check logs

```bash
docker logs -f backend
docker logs -f frontend
docker logs -f proxy
```
---

### API endpoints

| Method | Endpoint     | Description        |
| ------ | ------------ | ------------------ |
| GET    | /api/message | Fetch all messages |
| POST   | /api/add     | Add a new message  |

Example using curl:

```bash
curl -X POST http://localhost:8081/api/add \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from Docker!"}'

curl http://localhost:8081/api/message
```
---

### Architecture Diagram

[Browser] -> [NGINX Proxy] -> [Backend API] -> [PostgreSQL]

- **Frontend:** 8080

- **Backend:** 5000

- **Proxy:** 8081

- **Database:** 5432

- **Frontend Access**-
Local frontend:: http://localhost:8080

Proxy with backend integration: http://localhost:8081