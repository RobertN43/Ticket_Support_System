from fastapi import FastAPI

from database import Base, engine

# Učitavamo modele da SQLAlchemy zna za njih
from models.department import Department
from models.position import Position
from models.employee import Employee
from models.ticket import Ticket
from models.comment import Comment
from models.ticket_history import TicketHistory


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}