
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import get_current_user


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# SLA targets in hours
SLA_HOURS = {
    "high": 4,
    "medium": 24,
    "low": 72
}


# Helper function: Create audit log
def create_audit_log(
    db: Session,
    ticket_id: int,
    action: str,
    changed_by_id: int,
    old_value: str | None = None,
    new_value: str | None = None
):
    audit_log = models.TicketAuditLog(
        ticket_id=ticket_id,
        changed_by_id=changed_by_id,
        action=action,
        old_value=old_value,
        new_value=new_value
    )

    db.add(audit_log)


# 1. Create a new ticket
@router.post("/", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_ticket = models.Ticket(
        subject=ticket.subject,
        description=ticket.description,
        priority=ticket.priority,
        created_by_id=current_user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    create_audit_log(
        db=db,
        ticket_id=new_ticket.id,
        changed_by_id=current_user.id,
        action="Ticket Created",
        new_value=new_ticket.subject
    )

    db.commit()

    return new_ticket


# 2. Get all tickets with search and filters
@router.get("/", response_model=list[schemas.TicketResponse])
def get_tickets(
    status: str | None = None,
    priority: str | None = None,
    assigned_to_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Ticket)

    if current_user.role == "customer":
        query = query.filter(
            models.Ticket.created_by_id == current_user.id
        )
    elif current_user.role != "support_agent":
        raise HTTPException(status_code=403, detail="Invalid user role")

    if status:
        if status not in ["open", "in_progress", "closed"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(models.Ticket.status == status)

    if priority:
        if priority not in ["low", "medium", "high"]:
            raise HTTPException(status_code=400, detail="Invalid priority")
        query = query.filter(models.Ticket.priority == priority)

    if assigned_to_id is not None:
        query = query.filter(
            models.Ticket.assigned_to_id == assigned_to_id
        )

    if search:
        query = query.filter(
            models.Ticket.subject.ilike(f"%{search}%")
        )

    return query.order_by(models.Ticket.created_at.desc()).all()


# 3. Get SLA status of a ticket
@router.get("/{ticket_id}/sla")
def get_ticket_sla(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == "customer":
        if ticket.created_by_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to view this ticket"
            )
    elif current_user.role != "support_agent":
        raise HTTPException(status_code=403, detail="Invalid user role")

    target_hours = SLA_HOURS[ticket.priority]
    created_at = ticket.created_at

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    deadline = created_at + timedelta(hours=target_hours)
    current_time = datetime.now(timezone.utc)

    if ticket.status == "closed":
        sla_status = "completed"
        remaining_seconds = None
        overdue_seconds = None
    elif current_time <= deadline:
        sla_status = "within_sla"
        remaining_seconds = int(
            (deadline - current_time).total_seconds()
        )
        overdue_seconds = None
    else:
        sla_status = "overdue"
        remaining_seconds = None
        overdue_seconds = int(
            (current_time - deadline).total_seconds()
        )

    return {
        "ticket_id": ticket.id,
        "priority": ticket.priority,
        "target_hours": target_hours,
        "created_at": created_at,
        "deadline": deadline,
        "checked_at": current_time,
        "sla_status": sla_status,
        "remaining_seconds": remaining_seconds,
        "overdue_seconds": overdue_seconds
    }


# 4. Get audit history of a ticket
@router.get("/{ticket_id}/audit-logs")
def get_ticket_audit_logs(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Customers can only view their own ticket history
    if current_user.role == "customer":
        if ticket.created_by_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to view this ticket history"
            )
    elif current_user.role != "support_agent":
        raise HTTPException(
            status_code=403,
            detail="Invalid user role"
        )

    logs = db.query(models.TicketAuditLog).filter(
        models.TicketAuditLog.ticket_id == ticket_id
    ).order_by(
        models.TicketAuditLog.created_at.asc()
    ).all()

    return [
        {
            "id": log.id,
            "ticket_id": log.ticket_id,
            "action": log.action,
            "old_value": log.old_value,
            "new_value": log.new_value,
            "changed_by_id": log.changed_by_id,
            "created_at": log.created_at
        }
        for log in logs
    ]


# 5. Get a single ticket
@router.get("/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if (
        current_user.role == "customer"
        and ticket.created_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this ticket"
        )

    return ticket


# 6. Update ticket with audit history
@router.put("/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_update: schemas.TicketUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if (
        current_user.role == "customer"
        and ticket.created_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this ticket"
        )

    if current_user.role == "customer":
        if "status" in ticket_update.model_fields_set:
            raise HTTPException(
                status_code=403,
                detail="Customers cannot change ticket status"
            )

        if "priority" in ticket_update.model_fields_set:
            raise HTTPException(
                status_code=403,
                detail="Customers cannot change ticket priority"
            )

    update_data = ticket_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        old_value = getattr(ticket, key)

        if old_value != value:
            create_audit_log(
                db=db,
                ticket_id=ticket.id,
                changed_by_id=current_user.id,
                action=f"{key.capitalize()} Changed",
                old_value=str(old_value) if old_value is not None else None,
                new_value=str(value) if value is not None else None
            )

            setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket


# 7. Delete a ticket
@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "support_agent":
        raise HTTPException(
            status_code=403,
            detail="Only support agents can delete tickets"
        )

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}


# 8. Assign ticket to a support agent
@router.put("/{ticket_id}/assign", response_model=schemas.TicketResponse)
def assign_ticket(
    ticket_id: int,
    assignment: schemas.TicketAssign,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "support_agent":
        raise HTTPException(
            status_code=403,
            detail="Only support agents can assign tickets"
        )

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    agent = db.query(models.User).filter(
        models.User.id == assignment.assigned_to_id,
        models.User.role == "support_agent"
    ).first()

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Support agent not found"
        )

    old_agent_id = ticket.assigned_to_id

    if old_agent_id != agent.id:
        ticket.assigned_to_id = agent.id

        create_audit_log(
            db=db,
            ticket_id=ticket.id,
            changed_by_id=current_user.id,
            action="Ticket Assigned",
            old_value=str(old_agent_id) if old_agent_id is not None else None,
            new_value=str(agent.id)
        )

    db.commit()
    db.refresh(ticket)

    return ticket
