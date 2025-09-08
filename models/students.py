from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    student_number = Column(Integer, nullable=False)
    password = Column(String, nullable=False)

    borrow = relationship("Borrow", back_populates="user")

    def __init__(self, username, student_number, password):
        self.username = username
        self.student_number = student_number
        self.password = password
