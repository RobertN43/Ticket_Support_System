
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models.ticket import Ticket
from models.employee import Employee


# Define the request body for creating a ticket
class TicketCreate(BaseModel):
    title: str
    description: str
    created_by: int
    assigned_to: int | None = None


# Define the request body for updating a ticket
class TicketUpdate(BaseModel):
    title: str
    description: str
    status: str
    assigned_to: int | None = None


# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for ticket-related endpoints
router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# GET all tickets
@router.get("")
def get_tickets(db=Depends(get_db)):
    tickets = db.query(Ticket).all()

    return tickets


# GET a single ticket by ID
@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db=Depends(get_db)
):
    ticket = db.query(Ticket).filter_by(
        id=ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


# POST a new ticket
@router.post("")
def create_ticket(
    ticket_data: TicketCreate,
    db=Depends(get_db)
):
    # Check if the employee creating the ticket exists
    creator = db.query(Employee).filter_by(
        id=ticket_data.created_by
    ).first()

    if creator is None:
        raise HTTPException(
            status_code=404,
            detail="Creator employee not found"
        )

    # Check if the assigned employee exists
    if ticket_data.assigned_to is not None:
        technician = db.query(Employee).filter_by(
            id=ticket_data.assigned_to
        ).first()

        if technician is None:
            raise HTTPException(
                status_code=404,
                detail="Assigned employee not found"
            )

    # Create a new ticket
    new_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        status="OPEN",
        created_by=ticket_data.created_by,
        assigned_to=ticket_data.assigned_to
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# PUT a ticket by ID
@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db=Depends(get_db)
):
    # Find the ticket
    ticket = db.query(Ticket).filter_by(
        id=ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Check if the assigned employee exists
    if ticket_data.assigned_to is not None:
        technician = db.query(Employee).filter_by(
            id=ticket_data.assigned_to
        ).first()

        if technician is None:
            raise HTTPException(
                status_code=404,
                detail="Assigned employee not found"
            )

    # Update ticket data
    ticket.title = ticket_data.title
    ticket.description = ticket_data.description
    ticket.status = ticket_data.status
    ticket.assigned_to = ticket_data.assigned_to

    db.commit()
    db.refresh(ticket)

    return ticket


# DELETE a ticket by ID
@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db=Depends(get_db)
):
    # Find the ticket
    ticket = db.query(Ticket).filter_by(
        id=ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }

