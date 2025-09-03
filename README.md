# Checkout System Architecture

This project is a reservation checkout system built with a modern, decoupled architecture.

## Technology Stack

*   **Backend Framework:** FastAPI (Python)
*   **Database:** Supabase (PostgreSQL)
*   **Message Queue:** TBD (Likely AWS SQS or RabbitMQ)
*   **Deployment:** Docker / Serverless (e.g., AWS Lambda for workers)

## Architecture Overview

The system uses a **Queue and Worker** pattern to handle checkouts asynchronously.

1.  **API (Producer):** A FastAPI endpoint receives the `/checkout` request. It performs basic validation, creates a job, and publishes it to a message queue. It responds immediately with a `202 Accepted` status.

2.  **Message Queue:** A central queue (like SQS) holds the checkout jobs. This decouples the API from the processing logic, ensuring resilience and scalability.

3.  **Database:** A Supabase (Postgres) instance acts as the source of truth. The core table is `reservations`, which includes a `status` column (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`) to track the state of each checkout.

4.  **Workers (Consumers):** These are independent background services (e.g., Docker containers or Lambda functions) that poll the message queue. When a job is received, a worker updates the reservation status to `PROCESSING`, calls the payment gateway, and finally updates the status to `COMPLETED` or `FAILED`.


## Project Structure

.
├── config/...                                   # configuration files and scripts, includes Docker
├── Makefile                                     # shortcuts for setup and common tasks
├── scripts/...                                  # helper scripts
├── pyproject.toml                               # tooling and environment config (uv)
├── ...
└── src/
    └── app/
        ├── domain/                              # domain layer
        │   ├── services/...                     # domain layer services
        │   ├── entities/...                     # entities (have identity)
        │   │   ├── base.py                      # base declarations
        │   │   └── ...                          # concrete entities
        │   ├── value_objects/...                # value objects (no identity)
        │   │   ├── base.py                      # base declarations
        │   │   └── ...                          # concrete value objects
        │   └── ...                              # ports, enums, exceptions, etc.
        │
        ├── application/...                      # application layer
        │   ├── commands/                        # write ops, business-critical reads
        │   │   ├── create_user.py               # interactor
        │   │   └── ...                          # other interactors
        │   ├── queries/                         # optimized read operations
        │   │   ├── list_users.py                # query service
        │   │   └── ...                          # other query services
        │   └── common/                          # common layer objects
        │       ├── services/...                 # authorization, etc.
        │       └── ...                          # ports, exceptions, etc.
        │
        ├── infrastructure/...                   # infrastructure layer
        │   ├── adapters/...                     # port adapters
        │   ├── auth/...                         # auth context (session-based)
        │   └── ...                              # persistence, exceptions, etc.
        │
        ├── presentation/...                     # presentation layer
        │   └── http/                            # http interface
        │       ├── auth/...                     # web auth logic
        │       ├── controllers/...              # controllers and routers
        │       └── errors/...                   # error handling helpers
        │
        ├── setup/
        │   ├── ioc/...                          # dependency injection setup
        │   ├── config/...                       # app settings
        │   └── app_factory.py                   # app builder
        │
        └── run.py                               # app entry point
