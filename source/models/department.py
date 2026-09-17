from database import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    positions = db.relationship("Position", backref="department")
    employees = db.relationship("Employee", backref="department")