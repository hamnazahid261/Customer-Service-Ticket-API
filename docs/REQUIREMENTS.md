# Customer Service Ticket API - Requirements

## 1. Project Overview

The Customer Service Ticket API is a backend application developed using Python, FastAPI, and PostgreSQL. It helps manage customer support requests through ticket creation, assignment, tracking, and auditing.

## 2. Functional Requirements

### User Management
- Users can register with their name, email, and password.
- Passwords must be securely hashed.
- Users can log in and receive a JWT access token.
- The system supports customer and support_agent roles.

### Authentication and Authorization
- Protected endpoints require JWT authentication.
- Users must have appropriate permissions to access resources.
- Customers cannot access other customers' private records.

### Ticket Management
- Authenticated customers can create tickets.
- Tickets contain a subject, description, status, and priority.
- Tickets can be assigned to support agents.
- Authorized users can view and update tickets.
- Tickets can be searched and filtered.

### SLA Monitoring
- The system calculates deadlines based on ticket priority.
- High priority: 4 hours.
- Medium priority: 24 hours.
- Low priority: 72 hours.
- The API reports whether a ticket is within SLA, overdue, or completed.

### Audit Logging
- The system records ticket creation, assignment, and updates.
- Audit records include the action, old value, new value, user ID, and timestamp.
- Authorized users can retrieve ticket audit history.

## 3. Non-Functional Requirements

### Security
- Password hashing.
- JWT-based authentication.
- Role-based access control.
- Protected API endpoints.

### Performance
- Database queries should retrieve relevant records efficiently.
- Search and filtering should support ticket management.

### Maintainability
- Code should be organized into separate modules.
- Database models and API schemas should be separated.
- API documentation should be available through Swagger UI.

### Reliability
- The API should validate incoming data.
- Errors should return appropriate HTTP status codes.
- Database resources should be properly managed.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM |
| Psycopg | PostgreSQL connection |
| JWT | Authentication |
| Pydantic | Data validation |
| Swagger UI | API testing and documentation |

## 5. User Roles

### Customer
- Register and log in.
- Create support tickets.
- View their own tickets.
- Access their own profile.

### Support Agent
- View all users.
- Assign tickets.
- Manage ticket updates according to permissions.
- Access authorized ticket information and audit history.

## 6. Project Scope

The project focuses on backend API development. It provides the core functionality required to manage customer support tickets, authentication, authorization, SLA monitoring, and audit history.