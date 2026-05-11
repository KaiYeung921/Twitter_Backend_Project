# Twitter Clone - Big Data Final Project
[![CI](https://github.com/KaiYeung921/Twitter_Backend_Project/actions/workflows/test.yml/badge.svg)](https://github.com/KaiYeung921/Twitter_Backend_Project/actions/workflows/test.yml)


## Overview
A full-stack Twitter clone built from scratch as the final project for CMC's Big Data course. The goal was to apply everything learned in the course into one production-ready web application — from database design to containerized deployment.

The core engineering challenge was making every page load in milliseconds against a database with over 1,000,000 rows. This required index design, query optimization, and understanding Postgres.


## Tech Stack
- **Flask** — Python web framework
- **PostgreSQL** — relational database with advanced indexing
- **psycopg2** — raw SQL queries (no ORM) for full control over performance
- **Docker + Docker Compose** — containerized dev and production environments
- **Nginx + Gunicorn** — web serving
- **GitHub Actions** — CI/CD pipeline that builds and tests containers on every push


## Build Instructions

### Development
```bash
docker compose up -d --build

