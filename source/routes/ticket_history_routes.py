
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models.ticket_history import TicketHistory
from models.ticket import Ticket
from models.employee import Employee


# Define the request body for creating a history entry
class TicketHistoryCreate(BaseModel):
    action: str
    ticket_id: int
    employee_id: int


# Define the request body for updating a history entry
class TicketHistoryUpdate(BaseModel):
    action: str


# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for ticket history-related endpoints
router = APIRouter(
    prefix="/ticket-history",
    tags=["Ticket History"]
)


# GET all history entries
@router.get("")
def get_history(db=Depends(get_db)):
    history = db.query(TicketHistory).all()

    return history


# GET a single history entry by ID
@router.get("/{history_id}")
def get_history_entry(
    history_id: int,
    db=Depends(get_db)
):
    history_entry = db.query(TicketHistory).filter_by(
        id=history_id
    ).first()

    if history_entry is None:
        raise HTTPException(
            status_code=404,
            detail="History entry not found"
        )

    return history_entry


# POST a new history entry
@router.post("")
def create_history_entry(
    history_data: TicketHistoryCreate,
    db=Depends(get_db)
):
    # Check if the ticket exists
    ticket = db.query(Ticket).filter_by(
        id=history_data.ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Check if the employee exists
    employee = db.query(Employee).filter_by(
        id=history_data.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Create a new history entry
    new_history = TicketHistory(
        action=history_data.action,
        ticket_id=history_data.ticket_id,
        employee_id=history_data.employee_id
    )

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return new_history


# PUT a history entry by ID
@router.put("/{history_id}")
def update_history_entry(
    history_id: int,
    history_data: TicketHistoryUpdate,
    db=Depends(get_db)
):
    history_entry = db.query(TicketHistory).filter_by(
        id=history_id
    ).first()

    if history_entry is None:
        raise HTTPException(
            status_code=404,
            detail="History entry not found"
        )

    history_entry.action = history_data.action

    db.commit()
    db.refresh(history_entry)

    return history_entry


# DELETE a history entry by ID
@router.delete("/{history_id}")
def delete_history_entry(
    history_id: int,
    db=Depends(get_db)
):
    history_entry = db.query(TicketHistory).filter_by(
        id=history_id
    ).first()

    if history_entry is None:
        raise HTTPException(
            status_code=404,
            detail="History entry not found"
        )

    db.delete(history_entry)
    db.commit()

    return {
        "message": "History entry deleted successfully"
    }
