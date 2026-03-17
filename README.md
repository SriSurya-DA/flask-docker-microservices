# Scalable Flask Application Deployment with Nginx Load Balancing using Docker Compose

This project is a simple practice setup to understand how a real backend application can be deployed using Docker.

The application is written in Python using Flask and is containerized using Docker.
Two instances of the Flask app are started to simulate scaling and basic load balancing.

Nginx is used as a reverse proxy to receive user requests and forward them to the running Flask containers.

MySQL is used as the database and Redis is added as a caching service.
Docker Compose is used to run and manage all the containers together.

---

## Project Components

* Flask application (Python backend)
* Nginx (reverse proxy and load balancer)
* MySQL (database with persistent volume)
* Redis (in-memory cache)
* Docker & Docker Compose (container orchestration)

---

## Folder Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── app.py
├── requirements.txt
├── nginx/
│   └── nginx.conf
└── db-init/
    └── init.sql
```

---

## How it Works

When the project is started, Docker Compose will:

* Build the Flask application image
* Start two Flask containers (app1 and app2)
* Start MySQL and create the required database
* Start Redis service
* Start Nginx and expose it on port 8080

All services communicate using the default Docker network.

User requests first reach Nginx and then get forwarded to one of the Flask containers.

---

## Running the Project

Make sure Docker and Docker Compose are installed.

Start the application using:

```
docker compose up --build
```

After the containers are up, open the browser and access:

```
http://localhost:8080
```

---

## Notes

* MySQL data is stored in a Docker volume so it will not be lost when containers restart.
* Database initialization scripts can be placed inside the `db-init` folder.
* Nginx configuration is mounted using a bind volume so it can be edited without rebuilding the image.
* This setup is mainly created for learning Docker networking, reverse proxy, and multi-container deployment.

---

## Learning Purpose

This project was created to practice:

* Docker image creation
* Docker Compose multi-service setup
* Basic load balancing using Nginx
* Service-to-service communication
* Environment variable configuration
* Simple microservices style deployment

---
