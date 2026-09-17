from flask import Blueprint

department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/departments"
)