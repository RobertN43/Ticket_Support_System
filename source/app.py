from flask import Flask
from database import db

from models.department import Department
from models.position import Position
from models.employee import Employee
from models.ticket import Ticket
from models.comment import Comment
from models.ticket_history import TicketHistory


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)