from fastapi import FastAPI
from database import Base, engine

# Loading SQLAlchemy models
from models.department import Department
from models.position import Position
from models.employee import Employee
from models.ticket import Ticket
from models.comment import Comment
from models.ticket_history import TicketHistory

from routes.department_routes import router as department_router
from routes.position_routes import router as position_router
from routes.employee_routes import router as employee_router
from routes.ticket_routes import router as ticket_router
from routes.comment_routes import router as comment_router
from routes.ticket_history_routes import router as ticket_history_router


Base.metadata.create_all(bind=engine)


app = FastAPI()

# Register routers
app.include_router(department_router)
app.include_router(position_router)
app.include_router(employee_router)
app.include_router(ticket_router)
app.include_router(comment_router)
app.include_router(ticket_history_router)


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}