from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # Application role: ADMIN, TECHNICIAN, WORKER
    role = Column(String(50), nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    position_id = Column(
        Integer,
        ForeignKey("positions.id"),
        nullable=False
    )

    created_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.created_by",
        backref="creator"
    )

    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to",
        backref="technician"
    )

    comments = relationship(
        "Comment",
        backref="employee"
    )

    history_entries = relationship(
        "TicketHistory",
        backref="employee"
    )