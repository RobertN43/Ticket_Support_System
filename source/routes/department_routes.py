from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from models.department import Department


# Define the request body structure
class DepartmentCreate(BaseModel):
    name: str
# Define the request body for updating a department
class DepartmentUpdate(BaseModel):
    name: str

# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for department-related endpoints
router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# GET all departments
@router.get("")
def get_departments(db=Depends(get_db)):
    departments = db.query(Department).all()

    return departments


# GET a single department by ID
@router.get("/{department_id}")
def get_department(department_id: int, db=Depends(get_db)):
    # Find the department with the requested ID
    department = db.query(Department).filter_by(id=department_id).first()

    # Return 404 if the department does not exist
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Return the department
    return department

# POST a new department
@router.post("")
def create_department(
    department: DepartmentCreate,
    db=Depends(get_db)
):
    # Create a new database object
    new_department = Department(
        name=department.name
    )

    # Add the object to the database session
    db.add(new_department)

    # Save changes to the database
    db.commit()

    # Refresh the object with database-generated values
    db.refresh(new_department)

    # Return the created department
    return new_department

# PUT a department by ID
@router.put("/{department_id}")
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db=Depends(get_db)
):
    # Find the department by ID
    department = db.query(Department).filter_by(id=department_id).first()

    # Return 404 if the department does not exist
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Update the department name
    department.name = department_data.name

    # Save changes to the database
    db.commit()

    # Refresh the object with the latest database values
    db.refresh(department)

    # Return the updated department
    return department

# DELETE a department by ID
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db=Depends(get_db)
):
    # Find the department by ID
    department = db.query(Department).filter_by(id=department_id).first()

    # Return 404 if the department does not exist
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    # Delete the department from the database
    db.delete(department)

    # Save the change to the database
    db.commit()

    # Return a confirmation message
    return {
        "message": "Department deleted successfully"
    }