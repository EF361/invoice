# Invoice Management System ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-2.2.5-green) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue) ![License](https://img.shields.io/badge/License-MIT-yellowgreen)

## Executive Summary
`invoice` is a robust, enterprise-grade financial management platform that enables businesses to handle invoicing with precision, security, and scalability. Designed to integrate seamlessly with QuickBooks and Xero, the system ensures compliance with financial best practices, immutability, and audit integrity, while maintaining high performance.

---

## Key Features
- **Currency-Aware Decimal Arithmetic**: Models money using decimal types with explicit rounding rules to prevent floating-point errors.
- **Secure Envelope Encryption**: Implements a managed KMS-backed encryption strategy to secure payment and invoice data.
- **ACID-Compliant Transactions**: Guarantees atomic, consistent, isolated, and durable invoice and payment processing.
- **Idempotent API Design**: Ensures retry-safe operations with idempotency keys, request hashing, and protection against replays.
- **Integrations with QuickBooks and Xero**:
  - Sandbox contract tests covering token rotation, rate limits, retries, and webhooks.
  - Automated data reconciliation between systems.
- **Audit Trail Integrity**: Secures logs with role-based access, hash-chaining, external immutable storage, and monitoring.
- **Resiliency and Disaster Recovery**: Detailed procedures for migrations, backups, restores, and failure recovery.
- **Scheduled Jobs**: Automates recurring billing and report generation with fine-grained logging via Loggly.

---

## Architecture & Workflow

```mermaid
flowchart TD
    A["Client Request (API)"] -->|"Validate Idempotency"| B["Idempotency Store (PostgreSQL)"]
    B -->|New Request| C["OpenAPI Validation (Flask)"]
    C -->|"Decrypt Data Key"| D["Key Management System (KMS)"]
    D -->|"Decrypt Invoice Data"| E["Data Layer (PostgreSQL)"]
    E -->|"Perform ACID Process"| F["Invoice Transaction"]
    F -->|"Persist Logs"| G["Audit Trail (Hash-Chained)"]
    F -->|"Push Events"| H["External Accounting Adapters"]
    H -->|"Integrate via API"| I["QuickBooks/Xero"]
    I -->|"Reconciliation and Acknowledgment"| J["Response to Client"]
```

---

## Tech Stack & Tools Breakdown
- **Programming Language**: Python 3.10
- **Web Framework**: Flask 2.2.5
- **Database**: PostgreSQL 14 with role-based security and Alembic migrations
- **Security**: Fernet for envelope encryption with KMS-backed design
- **APIs**: OpenAPI 3.0 with QuickBooks and Xero integrations
- **Testing**: Contract tests with `pytest`
- **Logging and Monitoring**: Loggly for centralized log analysis
- **Scheduling**: Automated jobs for recurring billing and reconciliation using Celery

---

## Installation & Quickstart

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/EF361/invoice.git
   cd invoice
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Define application-specific secrets and environment configurations:
   ```bash
   export FLASK_ENV=development
   export DATABASE_URL=postgresql://user:password@localhost/invoice_db
   export KMS_ENDPOINT=https://your-kms-endpoint
   export LOGGLY_TOKEN=your-loggly-token
   ```

5. **Apply Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Run the Application**:
   ```bash
   flask run
   ```

7. **Run Tests**:
   ```bash
   pytest
   ```

---

## Security & Compliance
1. **Encryption**: All sensitive data is encrypted with a managed KMS-backed envelope encryption strategy for PCI-DSS and GDPR compliance.
2. **Audit**: Immutable audit logs are hash-chained and/or stored in immutable external storage.
3. **Testing**: Comprehensive suite of sandbox contract tests for error-prone external integrations (QuickBooks, Xero).

---

## Planned Improvements
- Upgrade dependencies to latest stable versions (e.g., Flask 3.x, PostgreSQL 15).
- Enhance reconciliation tooling with detailed mismatch reports.
- Introduce multi-region failover for added resiliency and backups.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.