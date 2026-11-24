# Customer Service Ticket API

A RESTful backend application developed using Python, FastAPI, and PostgreSQL to manage customer support tickets.

## 1. Project Overview

The Customer Service Ticket API allows customers to submit support tickets and support agents to manage, assign, update, and track them.

The application includes authentication, role-based access control, ticket management, search and filtering, SLA tracking, and audit logging.

## 2. Features

- Customer registration and login
- Password hashing
- JWT-based authentication
- Role-based access control (Customer and Support Agent)
- Create and view support tickets
- Update ticket information
- Assign tickets to support agents
- Search tickets by subject
- Filter tickets by status, priority, and assigned agent
- SLA deadline tracking
- Ticket activity and audit history
- PostgreSQL database integration

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database ORM |
| Pydantic | Request and response validation |
| JWT | Authentication |
| Pytest | Automated testing |

## 4. Project Structure

```text
Customer_Service_Ticket_API/
│
├── app/
│   ├── routers/
│   │   ├── tickets.py
│   │   ├── users.py
│   │   └── auth.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── main.py
│
├── docs/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 5. Database Design

Database Name: `customer_service_db`

Main database tables:

- **users:** Stores customer and support agent information.
- **tickets:** Stores ticket subjects, descriptions, priorities, statuses, and assignments.
- **ticket_audit_logs:** Stores ticket activity history, including changes and timestamps.

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Customer_Service_Ticket_API
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root.

Add your own PostgreSQL connection string and a secure secret key:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/customer_service_db
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not upload real passwords or secret keys to GitHub.

### Step 5: Create the PostgreSQL database

Create a database named:

```sql
CREATE DATABASE customer_service_db;
```

### Step 6: Run the application

On Windows PowerShell:

```powershell
$env:PSYCOPG_IMPL = "python"
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 7. API Documentation

FastAPI provides interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Authentication Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/users/` | Register a customer |
| POST | `/auth/login` | Authenticate and receive JWT |

### Ticket Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/tickets/` | Create a ticket |
| GET | `/tickets/` | Retrieve tickets |
| GET | `/tickets/{ticket_id}` | Retrieve a specific ticket |
| PUT | `/tickets/{ticket_id}` | Update ticket information |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket |
| PUT | `/tickets/{ticket_id}/assign` | Assign ticket to an agent |
| GET | `/tickets/{ticket_id}/sla` | Check SLA status |
| GET | `/tickets/{ticket_id}/audit-logs` | View ticket activity history |

### User Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/users/` | Retrieve all users (support agent only) |
| GET | `/users/{user_id}` | Retrieve a user profile |

## 8. Search and Filtering

The ticket listing endpoint supports:

- `search`: Search ticket subjects.
- `status`: Filter by ticket status.
- `priority`: Filter by ticket priority.
- `assigned_to_id`: Filter by assigned support agent.

Example:

```text
GET /tickets/?search=login&priority=high
```

## 9. Authentication and Authorization

The application uses JWT authentication to protect API endpoints.

User roles:

- **Customer:** Can create tickets and access their own tickets.
- **Support Agent:** Can manage tickets, assign tickets, and access user information.

Customers cannot change ticket priority or status and cannot access other customers' tickets.

## 10. SLA Tracking

The application uses priority-based SLA targets:

| Priority | SLA Target |
|---|---:|
| High | 4 hours |
| Medium | 24 hours |
| Low | 72 hours |

SLA endpoint reports whether a ticket is within its deadline, overdue, or completed.

These are the project's configured targets, not an external industry standard.

## 11. Audit Logging

The application records important ticket activities, including:

- Ticket creation
- Ticket assignment
- Subject changes
- Description changes
- Priority changes
- Status changes

Audit history can be retrieved through:

```text
GET /tickets/{ticket_id}/audit-logs
```

## 12. Testing

The project includes automated API tests using Pytest and FastAPI TestClient.

### Run Automated Tests

Execute the following command from the project root:

```bash
python -m pytest -v
```

### Current Test Coverage

The automated test suite verifies:

- Home endpoint returns HTTP 200 and the expected response message.
- OpenAPI schema is accessible and contains the correct project title.
- Swagger documentation endpoint is accessible.

**Latest Test Result:** 3 tests passed successfully.

The API can also be explored manually through Swagger UI at `/docs`.

## 13. Future Improvements

- Automated API test coverage
- Pagination for ticket listing
- More detailed reporting and analytics
- Improved SLA configuration
- Additional audit and administrative features

## 14. Conclusion

The Customer Service Ticket API provides a structured backend solution for managing customer support requests using FastAPI and PostgreSQL. It demonstrates REST API development, database integration, authentication, authorization, ticket management, SLA tracking, and audit logging.