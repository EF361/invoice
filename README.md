# Invoice Manager

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.5-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Tests](https://img.shields.io/badge/Tests-Passing-green)

## Executive Summary

Invoice Manager is a secure, auditable, and scalable invoicing system built to manage financial transactions and integrations with QuickBooks and Xero. It focuses on enterprise-grade encryption, compliance, and immutability for financial operations.

## Key Features

### Implemented
- **Immutable Audit Trails**: Append-only logging backed by database permissions ensures transactional integrity and compliance.
- **PostgreSQL Transactions**: Reliable, ACID-compliant invoice creation and billing processes.
- **Idempotency Handling**: Defined uniqueness constraints and idempotency-key lifecycle to prevent duplicate invoice generation during retries.
- **Envelope Encryption**: Managed key identifiers with tested rotation procedures; sensitive data encryption handled via `Fernet`. No logging of plaintext financial or authentication data.
- **OpenAPI 3.0 Documentation**: Complete, interactive API schema for fast developer onboarding.
- **Recurring Billing**: Job scheduling for automated invoice generation on configurable cycles.
- **Granular Concurrency Controls**: Optimized transactions to handle concurrent invoice processing safely.
- **Decimal-First Calculations**: Accurate handling of tax and currency calculations with precision validated at each step.

### In Progress
- **Advanced Contract Testing**: Validating integration with QuickBooks and Xero sandbox environments for edge cases like rate limits, expired tokens, and reconciliation mismatches.
- **Field-Level Encryption**: Extending security with granular control over sensitive fields.
- **Jurisdiction-Specific Tax Rules**: Explicit versioning and rounding tests for compliance across U.S. and international tax codes.

### Roadmap
- Enhanced **Audit Semantics**: Leveraging third-party append-only storage for tamper-proof compliance.
- Integration with additional accounting platforms and expanded support for region-specific regulations.

## Architecture & Workflow

```mermaid
graph TD
    A[Client Request] -->|API Call| B[Flask (REST API)]
    B -->|Validation| C[Business Logic]
    C -->|Transaction Begins| D[PostgreSQL Database]
    D -->|Insert Invoice| E[Immutable Audit Trail]
    E -->|Key Encryption| F[Encryption Service (Fernet)]
    C -->|Adapter| G[QuickBooks/Xero API]
    G -->|Response| C
    C -->|Transaction Commit| H[Success Response]
    C -->|Error Handling| I[Retry Logic / Rollback]
    I -->|404 or 500| J[Error Response]
```

## Tech Stack & Tools Breakdown

- **Backend Framework**: Flask - Lightweight and fast REST API development.
- **Database**: PostgreSQL - Fully ACID-compliant relational database.
- **ORM & Migrations**: Alembic - Schema management and versioning.
- **Encryption**: Fernet - Envelope encryption; key management and rotation.
- **API Integration**: QuickBooks & Xero APIs - Accounting system adapters.
- **Testing Framework**: Pytest - Component and integration test validation.
- **Schema & Docs**: OpenAPI 3.0 - API design for developer-friendly documentation.
- **Logging**: Loggly - Trace invoice workflows and error events.

## Quickstart

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/EF361/invoice.git
   cd invoice
   ```

2. Set up a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your PostgreSQL, encryption, and API credentials.

5. Run PostgreSQL migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the Flask app:
   ```bash
   flask run
   ```

### Run Tests
To execute the test suite:
```bash
pytest
```

## Contributions
We welcome contributions from the community! Please review our `CONTRIBUTING.md` guidelines before submitting a pull request.

---

Invoice Manager © 2023 Alicia Goh (EF361). Licensed under MIT.