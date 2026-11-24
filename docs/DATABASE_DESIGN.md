# Customer Service Ticket API - Database Design

## 1. Database Overview

The project uses PostgreSQL as its relational database and SQLAlchemy as its ORM.

The database contains three main tables:

1. `users`
2. `tickets`
3. `ticket_audit_logs`

## 2. Users Table

The `users` table stores customer and support agent information.

| Column | Description |
|---|---|
| id | Primary key |
| name | User's full name |
| email | User's unique email address |
| role | User role: customer or support_agent |
| password_hash | Securely hashed password |

### User Roles
- `customer`
- `support_agent`

New registrations are assigned the customer role by default.

## 3. Tickets Table

The `tickets` table stores customer support requests.

| Column | Description |
|---|---|
| id | Primary key |
| subject | Ticket subject |
| description | Detailed issue description |
| status | Current ticket status |
| priority | Ticket priority |
| created_by_id | Foreign key referencing users.id |
| assigned_to_id | Nullable foreign key referencing users.id |
| created_at | Ticket creation timestamp |
| updated_at | Last update timestamp |

### Ticket Status Values
- `open`
- `in_progress`
- `closed`

### Ticket Priority Values
- `low`
- `medium`
- `high`

## 4. Ticket Audit Logs Table

The `ticket_audit_logs` table maintains a history of important ticket changes.

| Column | Description |
|---|---|
| id | Primary key |
| ticket_id | Foreign key referencing tickets.id |
| changed_by_id | Nullable foreign key referencing users.id |
| action | Description of the performed action |
| old_value | Previous value |
| new_value | Updated value |
| created_at | Date and time of the activity |

Audit logs help track ticket creation, assignment, and updates.

## 5. Table Relationships

### Users and Tickets
- One user can create multiple tickets.
- Each ticket has one creator.
- A support agent can be assigned multiple tickets.
- A ticket may have no assigned agent.

### Tickets and Audit Logs
- One ticket can have multiple audit log records.
- Each audit record belongs to one ticket.

## 6. Relationship Summary

- `users.id` → `tickets.created_by_id`
- `users.id` → `tickets.assigned_to_id`
- `tickets.id` → `ticket_audit_logs.ticket_id`
- `users.id` → `ticket_audit_logs.changed_by_id`

## 7. Database Technology

- Database: PostgreSQL
- ORM: SQLAlchemy
- Backend: Python and FastAPI
- Database connection: Psycopg

## 8. Purpose of Database Design

This database structure supports:
- User authentication and role management.
- Ticket creation and assignment.
- Ticket status and priority management.
- Ticket search and filtering.
- SLA monitoring.
- Audit history and accountability.