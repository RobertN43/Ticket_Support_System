from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)

    created_by = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    assigned_to = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True
    )

    comments = relationship("Comment", backref="ticket")
    history = relationship("TicketHistory", backref="ticket")