
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models.employee import Employee


# Define the request body for creating an employee
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
    department_id: int
    position_id: int


# Define the request body for updating an employee
class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str
    department_id: int
    position_id: int


# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for employee-related endpoints
router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# GET all employees
@router.get("")
def get_employees(db=Depends(get_db)):
    employees = db.query(Employee).all()

    return employees


# GET a single employee by ID
@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    db=Depends(get_db)
):
    employee = db.query(Employee).filter_by(
        id=employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# POST a new employee
@router.post("")
def create_employee(
    employee_data: EmployeeCreate,
    db=Depends(get_db)
):
    # Check if the email is already in use
    existing_employee = db.query(Employee).filter_by(
        email=employee_data.email
    ).first()

    if existing_employee is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Create a new employee
    new_employee = Employee(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        password=employee_data.password,
        role=employee_data.role,
        department_id=employee_data.department_id,
        position_id=employee_data.position_id
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# PUT an employee by ID
@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db=Depends(get_db)
):
    employee = db.query(Employee).filter_by(
        id=employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update employee data
    employee.first_name = employee_data.first_name
    employee.last_name = employee_data.last_name
    employee.email = employee_data.email
    employee.role = employee_data.role
    employee.department_id = employee_data.department_id
    employee.position_id = employee_data.position_id

    db.commit()
    db.refresh(employee)

    return employee


# DELETE an employee by ID
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db=Depends(get_db)
):
    employee = db.query(Employee).filter_by(
        id=employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }

