from database import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    position_id = db.Column(
        db.Integer,
        db.ForeignKey("positions.id"),
        nullable=False
    )

    created_tickets = db.relationship(
        "Ticket",
        foreign_keys="Ticket.created_by",
        backref="creator"
    )

    assigned_tickets = db.relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to",
        backref="technician"
    )

    comments = db.relationship("Comment", backref="employee")
    history_entries = db.relationship("TicketHistory", backref="employee")