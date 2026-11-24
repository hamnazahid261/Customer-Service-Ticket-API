# Customer Service Ticket API - Workflow

## 1. User Registration
- A new user registers using name, email, and password.
- The system securely hashes the password before storing it.
- Every newly registered user is assigned the `customer` role.

## 2. User Login
- The user logs in using email and password.
- The system verifies the credentials.
- After successful login, a JWT access token is generated.
- The token is required to access protected endpoints.

## 3. Ticket Creation
- An authenticated customer creates a support ticket.
- The customer provides a subject, description, and priority.
- The system automatically assigns the logged-in user as the ticket creator.
- The default ticket status is `open`.
- A ticket creation audit record is generated.

## 4. Ticket Assignment
- A support agent can assign a ticket to an agent using the assignment endpoint.
- The assigned agent's user ID is stored in `assigned_to_id`.
- The assignment action is recorded in the audit logs.

## 5. Ticket Management
- Tickets can be viewed individually or through the ticket listing endpoint.
- Tickets can be filtered by status, priority, and assigned agent.
- Tickets can also be searched using the search parameter.
- Customers cannot change ticket status or priority.
- Support agents can manage ticket updates according to the implemented authorization rules.

## 6. Ticket Status
The system supports three ticket statuses:

- `open` - A newly created or open ticket.
- `in_progress` - A ticket currently being handled.
- `closed` - A ticket whose work has been completed.

## 7. SLA Monitoring
The system calculates SLA deadlines according to ticket priority:

| Priority | Configured SLA Target |
|---|---:|
| High | 4 hours |
| Medium | 24 hours |
| Low | 72 hours |

The SLA endpoint checks whether a ticket is within its configured target or overdue. Closed tickets are marked as completed.

## 8. Audit Logging
The system maintains an audit trail for important ticket activities, including:

- Ticket creation
- Ticket assignment
- Ticket field updates

Audit records store the action, previous value, new value, user who performed the change, and timestamp.

Users can retrieve the audit history of tickets they are authorized to access.

## 9. Role-Based Access Control

### Customer
- Register and log in.
- Create support tickets.
- View their own tickets.
- Access their own user profile.
- Cannot view all users or change ticket status and priority.

### Support Agent
- View all users.
- Access tickets according to the implemented permissions.
- Assign tickets.
- Manage ticket updates.
- View authorized ticket audit logs and SLA information.

## 10. Overall Workflow

User Registration → Login → JWT Authentication → Ticket Creation → Ticket Assignment → Ticket Management → SLA Monitoring → Ticket Closure → Audit History