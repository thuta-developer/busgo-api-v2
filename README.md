# BusGo — Production Bus Ticket System

A production-style bus ticket booking platform built with Django REST Framework + FastAPI microservices.

## Architecture

```text
Nginx (API Gateway)
  │
  ├── identity-service   (Django + DRF)      → identity_db
  ├── bus-service        (FastAPI)           → bus_db
  ├── booking-service    (FastAPI)           → booking_db
  ├── payment-service    (FastAPI + Celery)  → payment_db
  └── notification-service (FastAPI + Celery) → notification_db
  │
  ├── PostgreSQL
  └── Redis (cache, hold, broker)