from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models.position import Position
from models.department import Department


# Define the request body for creating a position
class PositionCreate(BaseModel):
    name: str
    department_id: int


# Define the request body for updating a position
class PositionUpdate(BaseModel):
    name: str
    department_id: int


# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for position-related endpoints
router = APIRouter(
    prefix="/positions",
    tags=["Positions"]
)


# GET all positions
@router.get("")
def get_positions(db=Depends(get_db)):
    # Get all positions from the database
    positions = db.query(Position).all()

    return positions


# GET a single position by ID
@router.get("/{position_id}")
def get_position(position_id: int, db=Depends(get_db)):
    # Find the position with the requested ID
    position = db.query(Position).filter_by(id=position_id).first()

    # Return 404 if the position does not exist
    if position is None:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )

    return position


# POST a new position
@router.post("")
def create_position(
    position_data: PositionCreate,
    db=Depends(get_db)
):
    # Check if the selected department exists
    department = db.query(Department).filter_by(
        id=position_data.department_id
    ).first()

    # Return 404 if the department does not exist
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Create a new position database object
    new_position = Position(
        name=position_data.name,
        department_id=position_data.department_id
    )

    # Add the new position to the database session
    db.add(new_position)

    # Save the new position to the database
    db.commit()

    # Refresh the object to get database-generated values
    db.refresh(new_position)

    return new_position


# PUT a position by ID
@router.put("/{position_id}")
def update_position(
    position_id: int,
    position_data: PositionUpdate,
    db=Depends(get_db)
):
    # Find the position by ID
    position = db.query(Position).filter_by(id=position_id).first()

    # Return 404 if the position does not exist
    if position is None:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )

    # Check if the new department exists
    department = db.query(Department).filter_by(
        id=position_data.department_id
    ).first()

    # Return 404 if the department does not exist
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Update the position data
    position.name = position_data.name
    position.department_id = position_data.department_id

    # Save the changes to the database
    db.commit()

    # Refresh the object with the latest database values
    db.refresh(position)

    return position


# DELETE a position by ID
@router.delete("/{position_id}")
def delete_position(
    position_id: int,
    db=Depends(get_db)
):
    # Find the position by ID
    position = db.query(Position).filter_by(id=position_id).first()

    # Return 404 if the position does not exist
    if position is None:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )

    # Delete the position from the database
    db.delete(position)

    # Save the deletion
    db.commit()

    return {
        "message": "Position deleted successfully"
    }