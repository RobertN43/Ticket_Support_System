from database import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=True
    )

    comments = db.relationship("Comment", backref="ticket")
    history = db.relationship("TicketHistory", backref="ticket")