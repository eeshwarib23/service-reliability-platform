# Service Reliability Platform (Mini)

A mini full-stack and SRE-focused platform that demonstrates how backend services
measure their own reliability through health checks, metrics, and observability.

This project is inspired by real production systems and SRE practices, including
latency tracking, error monitoring, throughput analysis, and runtime configuration.

---

## What this project demonstrates

- Backend API design using FastAPI
- SRE-style health and readiness endpoints
- Request latency, error rate, and throughput metrics
- Prometheus-compatible `/metrics` endpoint
- A lightweight web dashboard for observability
- Runtime configuration for latency and error injection
- Foundations of reliability engineering and monitoring

---

## Architecture (High Level)

Client / Dashboard  
→ REST API (FastAPI)  
→ Service Logic + Instrumentation  
→ In-memory Metrics Store  
→ Prometheus-style Metrics Endpoint  

---

## Core Endpoints

- `GET /health` – liveness check  
- `GET /ready` – readiness check  
- `POST /api/request` – simulated backend request  
- `GET /api/summary` – aggregated reliability metrics  
- `GET /metrics` – Prometheus-compatible metrics  

---

## Tech Stack

- Python
- FastAPI
- Prometheus Client
- HTML / JavaScript (Dashboard)
- GitHub Actions (planned)

---

This project is intentionally small but realistic.
It focuses on **how services observe themselves in production**, rather than
on UI polish or complex infrastructure.

It is meant to reflect real-world reliability and backend engineering patterns.

Eeshwari Balusu  
Software Engineer | SRE | Data & Quant Systems
