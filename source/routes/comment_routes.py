
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import SessionLocal
from models.comment import Comment
from models.ticket import Ticket
from models.employee import Employee


# Define the request body for creating a comment
class CommentCreate(BaseModel):
    content: str
    ticket_id: int
    employee_id: int


# Define the request body for updating a comment
class CommentUpdate(BaseModel):
    content: str


# Create a database session for the request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create a router for comment-related endpoints
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


# GET all comments
@router.get("")
def get_comments(db=Depends(get_db)):
    comments = db.query(Comment).all()

    return comments


# GET a single comment by ID
@router.get("/{comment_id}")
def get_comment(
    comment_id: int,
    db=Depends(get_db)
):
    comment = db.query(Comment).filter_by(
        id=comment_id
    ).first()

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment


# POST a new comment
@router.post("")
def create_comment(
    comment_data: CommentCreate,
    db=Depends(get_db)
):
    # Check if the ticket exists
    ticket = db.query(Ticket).filter_by(
        id=comment_data.ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Check if the employee exists
    employee = db.query(Employee).filter_by(
        id=comment_data.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Create a new comment
    new_comment = Comment(
        content=comment_data.content,
        ticket_id=comment_data.ticket_id,
        employee_id=comment_data.employee_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


# PUT a comment by ID
@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db=Depends(get_db)
):
    comment = db.query(Comment).filter_by(
        id=comment_id
    ).first()

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    comment.content = comment_data.content

    db.commit()
    db.refresh(comment)

    return comment


# DELETE a comment by ID
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db=Depends(get_db)
):
    comment = db.query(Comment).filter_by(
        id=comment_id
    ).first()

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db.delete(comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }

