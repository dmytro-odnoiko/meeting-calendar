from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db import Base

class User(Base):
   __tablename__ = "user"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(50))
   email = Column(String(50), unique=True, index=True)
   hashed_password = Column(Text, nullable=False)
   meetings = relationship("Meeting", back_populates="client",
                        cascade="all, delete-orphan")
