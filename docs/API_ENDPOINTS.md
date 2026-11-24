# Customer Service Ticket API - API Endpoints

## 1. Base URL

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 2. Authentication Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/auth/login` | Login and receive JWT token | Public |

## 3. User Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/users/` | Register a new customer | Public |
| GET | `/users/` | Get all users | Support Agent |
| GET | `/users/{user_id}` | Get a user's profile | Authenticated |

## 4. Ticket Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/tickets/` | Create a ticket | Authenticated |
| GET | `/tickets/` | List and filter tickets | Authenticated |
| GET | `/tickets/{ticket_id}` | Get ticket details | Authenticated |
| PUT | `/tickets/{ticket_id}` | Update a ticket | Authenticated, subject to role permissions |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket | Authenticated, subject to role permissions |
| PUT | `/tickets/{ticket_id}/assign` | Assign a ticket | Support Agent |
| GET | `/tickets/{ticket_id}/sla` | Check ticket SLA status | Authorized User |
| GET | `/tickets/{ticket_id}/audit-logs` | View ticket audit history | Authorized User |

## 5. Ticket Search and Filters

The `GET /tickets/` endpoint supports these query parameters:

| Parameter | Description |
|---|---|
| status | Filter tickets by status |
| priority | Filter tickets by priority |
| assigned_to_id | Filter by assigned agent |
| search | Search ticket text |

Example:

```text
GET /tickets/?priority=medium
GET /tickets/?status=open
GET /tickets/?assigned_to_id=2
GET /tickets/?search=login
```

Filters can also be combined.

## 6. Ticket Creation Example

Request:

```http
POST /tickets/
```

Example JSON:

```json
{
  "subject": "Login Issue",
  "description": "Unable to log in to my account",
  "priority": "high"
}
```

The creator is identified automatically from the authenticated user.

## 7. Login Example

Request:

```http
POST /auth/login
```

Example JSON:

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

A successful login returns a JWT access token.

Use this token in Swagger's Authorize option to access protected endpoints.

## 8. Ticket Status Values

- `open`
- `in_progress`
- `closed`

## 9. Ticket Priority Values

- `low`
- `medium`
- `high`

## 10. SLA Targets

| Priority | Configured Target |
|---|---:|
| High | 4 hours |
| Medium | 24 hours |
| Low | 72 hours |

## 11. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 401 | Authentication required or invalid |
| 403 | Permission denied |
| 404 | Resource not found |
| 422 | Validation error |

## 12. Authentication and Authorization

- JWT authentication protects restricted endpoints.
- Passwords are stored as hashes.
- Customers have restricted access to their own records and tickets.
- Support agents have additional management permissions.
- Unauthorized actions are rejected by the API.