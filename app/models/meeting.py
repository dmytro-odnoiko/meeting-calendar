from enum import Enum as StEnum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum,\
                       Boolean
from sqlalchemy.orm import relationship

from db import Base



class MeetingStatus(str, StEnum):
    created = 'created'
    modified = 'modified'
    canceled = 'canceled'


class Meeting(Base):
    __tablename__ = "meeting"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(255), index=True)
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    status = Column(Enum(MeetingStatus))
    notified = Column(Boolean, default=False)
    client_id = Column(Integer, ForeignKey("user.id"))

    client = relationship("User", back_populates="meetings")