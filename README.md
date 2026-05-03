# Flask on Docker

[![Continuous Integration](https://github.com/KaiYeung921/flask-on-docker/actions/workflows/main.yml/badge.svg)](https://github.com/KaiYeung921/flask-on-docker/actions/workflows/main.yml)

## Overview
This repository contains a containerized Flask application using a modified Instagram tech stack. The project utilizes **Gunicorn** as the production web server, **Nginx** as a reverse proxy to handle requests and serve static/media files, and **PostgreSQL** for persistent data storage. All services are orchestrated using Docker Compose to ensure a consistent environment from development to production.

## Demo
![Application Demo](Example.gif)

## Build Instructions

### 1. Prerequisites
* Docker and Docker Compose installed.
* A `.env.prod.db` file (and other required `.env` files) populated with your credentials. **Note: These are excluded from the repository for security.**

### 2. Environment Configuration
For security reasons, production credentials are not stored in this repository. You must create the following files in the root directory before launching the containers to avoid a `-2` point total penalty:

* `.env.prod`: General production settings (e.g., `FLASK_ENV=production`).
* `.env.prod.db`: Database credentials including `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.

### 3. Service Orchestration (CLI Commands)
From your terminal, navigate to the project root and execute the following sequence:

**A. Build and Start the Stack**
This command builds the custom images for Nginx and Flask and starts all services in the background:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
Then:
```bash
docker compose -f docker-compose.prod.yml exec web python manage.py create_db
```
### 4. Accessing the Servies
The application is exposed via Nginx on the host port specified in your compose file (default is 1080):

Main Application Interface: http://localhost:1080

Static Assets: Verify Nginx is serving static files at http://localhost:1080/static/hello.txt.

Media Uploads: View uploaded media files at http://localhost:1080/media/<filename>.

