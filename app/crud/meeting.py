from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import and_, or_

from models.meeting import MeetingStatus, Meeting
from db import SessionLocal

from schemas.meeting import Meeting as MeetingSchema
from schemas.user import UserBase as UserSchema

def check_meeting_time_booked(
    db: SessionLocal,
    meeting_data: MeetingSchema,
    meeting_id: int | None = None
):
    meeting_time_booked = db.query(Meeting).filter(
        or_(
            and_(Meeting.start_dt <= meeting_data.start_dt, 
                Meeting.end_dt >= meeting_data.start_dt),

            and_(Meeting.start_dt <= meeting_data.end_dt, 
                Meeting.end_dt >= meeting_data.end_dt),  

            and_(Meeting.start_dt > meeting_data.start_dt, 
                Meeting.end_dt < meeting_data.end_dt),
        ),
        Meeting.status != MeetingStatus.canceled
    )

    if meeting_id:
        meeting_time_booked = meeting_time_booked.\
            filter(Meeting.id != meeting_id)
    
    return meeting_time_booked.first()

def create_meeting(
    db: SessionLocal,
    current_user: UserSchema,
    meeting_data: MeetingSchema
):
    if check_meeting_time_booked(db, meeting_data):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail='This time already booked')
    new_meeting = Meeting(
        title = meeting_data.title,
        description = meeting_data.description,
        start_dt = meeting_data.start_dt,
        end_dt = meeting_data.end_dt,
        status = meeting_data.status,
        notified = False
    )
    new_meeting.client_id = current_user.id
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting
    
def update_meeting(
    db: SessionLocal, 
    meeting_id: int, 
    meeting_data: MeetingSchema,
    current_user: UserSchema
):  
    if check_meeting_time_booked(db, meeting_data, meeting_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='This time already booked')
    update_meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if current_user.id != update_meeting.client_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Access denied')
    update_meeting.title = meeting_data.title
    update_meeting.description = meeting_data.description
    update_meeting.start_dt = meeting_data.start_dt
    update_meeting.end_dt = meeting_data.end_dt
    update_meeting.status = meeting_data.status
    update_meeting.notified = False
    db.commit()
    db.refresh(update_meeting)
    return update_meeting

def get_meetings(db: SessionLocal, user_id: int):
    own_meetings = db.query(Meeting).filter(
            Meeting.client_id == user_id,
            Meeting.status != MeetingStatus.canceled,
            Meeting.start_dt >= datetime.today()
        ).all()
    other_client_meetings = db.query(Meeting).filter(
            Meeting.client_id != user_id,
            Meeting.status != MeetingStatus.canceled,
            Meeting.start_dt >= datetime.today()
        ).with_entities(Meeting.id, Meeting.start_dt, Meeting.end_dt).all()
    return {
        'own_meetings': (
            {
                'id' : meeting.id,
                'title': meeting.title,
                'description': meeting.description,
                'start_dt': meeting.start_dt,
                'end_dt': meeting.end_dt,
                'status': meeting.status,
                'client_id': meeting.client_id,
            }
            for meeting in own_meetings
        ),
        'other_client_meetings': (
            {
                'id' : meeting.id,
                'start_dt': meeting.start_dt,
                'end_dt': meeting.end_dt,
            } 
            for meeting in other_client_meetings
        )
    }