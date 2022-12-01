from datetime import datetime

from fastapi import Depends, APIRouter, BackgroundTasks

from typing import Union

from db import get_db, SessionLocal

from core.notification import send_in_background

from models.user import User

from schemas.meeting import MeetingsListResponse, MeetingResponse,\
   Meeting as MeetingSchema


from core.utils import get_current_user
from crud.meeting import create_meeting, update_meeting, get_meetings


router = APIRouter()


@router.get("/api/meetings", response_model=MeetingsListResponse)
def meetings(
   current_user: User = Depends(get_current_user),
   db: SessionLocal = Depends(get_db)
):
   """return a list of meetings"""
   meetings = get_meetings(db, current_user.id)
   return meetings

@router.post(
   "/api/meetings", 
   response_model=MeetingResponse,
   status_code=201
)
async def add_meeting(
      meeting_data: MeetingSchema,
      background_tasks: BackgroundTasks,
      current_user: User = Depends(get_current_user),
      db: SessionLocal = Depends(get_db),         
   ):
   """add a meeting"""
   meeting = create_meeting(db, current_user, meeting_data)
   await send_in_background(background_tasks, current_user.email, meeting_data)
   return {
      'id' : meeting.id,
      'title': meeting.title,
      'description': meeting.description,
      'start_dt': meeting.start_dt,
      'end_dt': meeting.end_dt,
      'status': meeting.status,
      'client_id': meeting.client_id,
   }

@router.put("/api/meetings/{meeting_id}", response_model=MeetingResponse)
async def put_meeting(
      meeting_id: int,
      meeting_data: MeetingSchema,
      background_tasks: BackgroundTasks,
      current_user: User = Depends(get_current_user),
      db: SessionLocal = Depends(get_db)
   ):
   """update and return meeting for given id"""
   updated_meeting = update_meeting(db, meeting_id, meeting_data, current_user)
   await send_in_background(background_tasks, current_user.email, meeting_data)
   return {
      'id' : updated_meeting.id,
      'title': updated_meeting.title,
      'description': updated_meeting.description,
      'start_dt': updated_meeting.start_dt,
      'end_dt': updated_meeting.end_dt,
      'status': updated_meeting.status,
      'client_id': updated_meeting.client_id,
   }