# ShopEase Order Service

A production-style e-commerce order management service built using **Podman, Flask, Gunicorn, PostgreSQL and Nginx**.

The project demonstrates containerization, multi-container development with Podman Compose, and staging deployment using `podman kube play`.

## Architecture

```text
                         Client
                           |
                           | :8081
                           v
                    +--------------+
                    | Nginx Gateway|
                    +--------------+
                       /        \
                      /          \
                     v            v
              +-----------+  +-----------+
              | Flask API |  | Frontend  |
              | Gunicorn  |  |   Nginx   |
              |   :5000   |  |   :8080   |
              +-----------+  +-----------+
                     |
                     v
              +-------------+
              | PostgreSQL  |
              |    :5432    |
              +-------------+
```


## Technologies

* Podman
* Podman Compose
* Podman Pods
* Flask
* Gunicorn
* PostgreSQL 16
* Nginx
* REST API
* Linux
* YAML
* Containerization

## Project Structure

```text
shopease-order-service-podman/
│
├── app/
│   ├── Containerfile
│   ├── app.py
│   └── requirements.txt
│
├── db/
│   ├── Containerfile
│   └── init.sql
│
├── frontend/
│   ├── Containerfile
│   ├── default.conf
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── nginx/
│   ├── Containerfile
│   └── default.conf.template
│
├── kube/
│   └── order-pod.yaml
│
├── compose.yaml
├── .gitignore
└── README.md
```

## Components

### Nginx Gateway

Nginx acts as the public entry point and reverse proxy.

```text
/api/*  → Flask API
/*      → Frontend
```

### Flask API

The backend provides REST APIs for order management.

```text
GET    /api/health
GET    /api/orders
GET    /api/orders/<id>
POST   /api/orders
PATCH  /api/orders/<id>
```

### PostgreSQL

PostgreSQL 16 stores order information.

The database is initialized with sample orders using `init.sql`.

### Frontend

The frontend is an HTML/CSS/JavaScript dashboard that displays:

* API status
* Database status
* Total orders
* Placed orders
* Shipped orders
* Delivered orders

## Container Images

```text
localhost/shopease-order-db:1.0
localhost/shopease-order-api:1.0
localhost/shopease-order-frontend:1.0
localhost/shopease-gateway:1.0
```

## Podman Compose Deployment

Start the application:

```bash
podman-compose up -d
```

Check containers:

```bash
podman ps
```

Compose gateway:

```text
http://localhost:8080
```

Health check:

```bash
curl http://localhost:8080/api/health
```

Expected:

```json
{"database":"connected","status":"ok"}
```

Stop the Compose deployment:

```bash
podman-compose down
```

## Pod Deployment

The application can also be deployed as a single multi-container Pod.

Start:

```bash
podman kube play kube/order-pod.yaml
```

Check Pod:

```bash
podman pod ps
```

Check containers:

```bash
podman ps --pod
```

The Pod gateway is exposed on:

```text
http://localhost:8081
```

## API Verification

### Health Check

```bash
curl http://localhost:8081/api/health
```

Expected:

```json
{"database":"connected","status":"ok"}
```

### Get Orders

```bash
curl http://localhost:8081/api/orders
```

### Create Order

```bash
curl -X POST http://localhost:8081/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"Gayatri Ramne","item":"Laptop Stand","quantity":1}'
```

### Update Order

```bash
curl -X PATCH http://localhost:8081/api/orders/4 \
  -H "Content-Type: application/json" \
  -d '{"status":"DELIVERED"}'
```

### Get Individual Order

```bash
curl http://localhost:8081/api/orders/4
```

## Frontend Verification

Open:

```text
http://localhost:8081
```

The ShopEase Order Dashboard should be displayed.

## Pod Networking

The Compose deployment uses service names:

```text
API → db
Gateway → api
Gateway → frontend
```

The Pod deployment uses a shared network namespace.

Therefore:

```text
API → PostgreSQL
127.0.0.1:5432

Gateway → API
127.0.0.1:5000

Gateway → Frontend
127.0.0.1:8080
```

This demonstrates the networking difference between separate containers in Compose and containers sharing a Pod network namespace.

## Verification Completed

The following were successfully tested:

* Pod creation
* Multi-container Pod deployment
* Nginx reverse proxy
* Frontend access
* Flask API
* Gunicorn
* PostgreSQL connectivity
* API health check
* GET orders
* POST orders
* PATCH order status
* Individual order retrieval
* Podman Compose deployment
* Podman Kubernetes-style deployment

## Learning Outcomes

Through this project, I gained hands-on experience with:

* Containerizing applications
* Creating Containerfiles
* Building Podman images
* Podman Compose
* Podman Pods
* Nginx reverse proxy
* Flask REST APIs
* Gunicorn
* PostgreSQL
* Container networking
* Health checks
* API testing with curl
* Kubernetes-style Pod YAML

## Author

**Gayatri Ramne**

DevOps / Cloud Engineer | RHCSA

## Special Thanks

Special thanks to **Ashutosh Bhakare Sir** and **Unnati Development & Training Centre** for the guidance, support and practical learning opportunities.

## Purpose

This project was created as a hands-on DevOps and containerization project for learning, practice and portfolio development.
