# Invoice Management System

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-red.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-In_Development-orange.svg)

## Executive Summary
The **Invoice Management System** streamlines invoicing, payment tracking, and accounting workflows for small and medium-sized businesses. It integrates seamlessly with QuickBooks and Xero APIs while ensuring financial correctness, auditability, and secure data handling.

---

## Key Features
- **Accurate Invoice Calculations**: Uses `decimal.Decimal` and explicit currency rules for precision.
- **Recurring Billing Support**: Schedule billing cycles with customizable intervals.
- **Enterprise-grade Security**: Field-level encryption using Fernet, with key rotation.
- **Immutable Audit Logs**: Ensures compliance through immutable, traceable financial records.
- **Idempotent APIs**: Guarantees safe retries and prevents duplicate transactions.
- **Custom Invoice Numbering**: Follows standardized, configurable numbering conventions.
- **Tax Handling**: Supports multiple tax regions and rates.
- **Integration Adapters**: Prebuilt connectors for QuickBooks and Xero, with robust validation.
- **OpenAPI Documentation**: Fully documented RESTful API with interactive Swagger UI.
- **Resilience & Testing**: Includes retry logic, concurrency handling, and fault-tolerant workflows.

---

## Architecture & Workflow

### High-level Workflow
> Modular, layered design ensures clear boundary separation between concerns.

```mermaid
flowchart TD
    A[Invoice Request] -->|REST API| B[API Layer]
    B -->|Validates & Extracts Data| C[Calculation & Business Logic Layer]
    C -->|Handles Taxation<br>Validations | D[Persistence Service]
    D -->|Stores Records Securely| E[PostgreSQL<br>(Encrypted Data)]
    C --> F[External Integrations]
    F -->|QuickBooks API| G[QuickBooks Sandbox]
    F -->|Xero API| H[Xero Sandbox]
    D --> I[Immutable Audit Logs]
    B -->|Schedules Jobs| J[Billing Scheduler]
```

### Key Architectural Components
1. **API Layer**: Serves as the gateway for RESTful transactions with validation, idempotency, and OpenAPI compliance.
2. **Calculation & Business Logic Layer**: Handles recursive billings, tax rules, and financial correctness.
3. **Persistence Service**: Manages encrypted database interactions and follows ACID compliance for transactions.
4. **External Adapters**: Isolated modules that ensure sandbox-verifiable operations with QuickBooks/Xero APIs.
5. **Audit Layer**: Maintains immutable and tamper-proof audit trails of key actions.
6. **Scheduled Tasks**: Runs background schedulers for recurring billing cycles.

---

## Tech Stack & Tools
- **Programming Language**: Python 3.10
- **Framework**: Flask (web framework)
- **Database**: PostgreSQL (encrypted fields with Fernet)
- **External APIs**: QuickBooks and Xero integrations
- **Testing & QA**:
  - **Pytest** for unit, functional, and concurrency tests
  - **Mock** for contract-based integration test coverage
- **Logging & Observability**:
  - Standard `logging` module for structured logs
  - Loggly for aggregated monitoring and error alerts
- **Specification & Standards**:
  - OpenAPI 3.0 for API design
  - Alembic for database migration management

---

## Quickstart / Installation

Follow these steps to set up and run the project locally:

### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [Docker](https://www.docker.com/) (optional, for API sandboxes)

### Installation Steps
1. **Clone Repository**
   ```bash
   git clone https://github.com/EF361/invoice.git
   cd invoice
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Rename `.env.example` to `.env` and update environment variables:
   ```plaintext
   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db_name>
   FERNET_KEY=<your_fernet_key>
   ```

4. **Database Migrations**
   ```bash
   flask db upgrade
   ```

5. **Run Application**
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

6. **Check API Documentation**
   Access `http://localhost:5000/api/docs` (Swagger UI).

7. **Run Tests**
   ```bash
   pytest
   ```

---

## Roadmap
### Upcoming Enhancements
1. **Advanced Security**:
   - Key rotation for Fernet encryption.
   - Field-specific encryption for sensitive data.
2. **Enhanced API Integrations**:
   - Support for additional accounting platforms (roadmap item).
3. **Financial Guarantees**:
   - Extend tax calculation for international compliance.
4. **Performance Improvements**:
   - Introduce horizontal scaling & caching for high-concurrency workloads.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing
We welcome contributions! Please check our [CONTRIBUTING](CONTRIBUTING.md) guide for submission details and join discussions in the Issues section.

---

**Crafted with precision by Alicia Goh ([EF361](https://github.com/EF361))**.