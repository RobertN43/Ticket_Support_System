from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    positions = relationship("Position", backref="department")
    employees = relationship("Employee", backref="department")