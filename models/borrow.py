from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Borrow(Base):
    __tablename__ = "borrow"

    borrow_id = Column("borrow_id", Integer, primary_key=True, autoincrement=True)
    student_id = Column("student_id", Integer, ForeignKey("students.id"), nullable=False)
    book_title = Column("book_title", String, nullable=False)
    book_writer = Column("book_writer", String, nullable=False)
    borrow_date = Column("borrow_date", DateTime, nullable=False)
    return_date = Column("return_date", DateTime, nullable=False)
    status = Column("status", String, nullable=False)

    user = relationship("Students", back_populates="borrow")

    def __init__(self, student_id, book_title, book_writer, borrow_date, return_date, status):
        self.student_id = student_id
        self.book_title = book_title
        self.book_writer = book_writer
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status