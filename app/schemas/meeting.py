from datetime import datetime, timezone

from pydantic import BaseModel, constr, conlist, validator

from models.meeting import MeetingStatus


class Meeting(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(min_length=3, max_length=255)
    start_dt: datetime
    end_dt: datetime
    status: MeetingStatus


    class Config:
        json_encoders = {
            'start_dt': lambda value: datetime.strptime(value, 
                            "%Y-%m-%dT%H:%M:%S"),
            'end_dt': lambda value: datetime.strptime(value, 
                            "%Y-%m-%dT%H:%M:%S"),
        }


    @staticmethod
    def get_current_interval():
        dt = datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        next_interval_date = None
        if dt.minute >= 30:
            next_interval_date = datetime(
                dt.year, dt.month, dt.day, dt.hour + 1, 0, 0, 0  
            )
        else:
            next_interval_date = datetime(
                dt.year, dt.month, dt.day, dt.hour, 30, 0, 0  
            )
        return next_interval_date
    
    
    @validator('start_dt', 'end_dt')
    def start_dt_validate(cls, v):
        if v < Meeting.get_current_interval():
            raise ValueError('Datetime value is less than posible value.')
        return v

    
    @validator('end_dt')
    def end_dt_validate(cls, v):
        if v < Meeting.get_current_interval():
            raise ValueError('Datetime value is less than posible value.')
        return v        
    
    
    @validator('end_dt')
    def compare_dts_validate(cls, v, values, **kwargs):
        if 'start_dt' in values and v <= values['start_dt']:
            raise ValueError(
                'Start datetime should be bigger than end datetime'
            )
        return v

class MeetingResponse(BaseModel):
    id : int
    title: constr(min_length=3, max_length=50) | None
    description: constr(min_length=3, max_length=50) | None
    start_dt: datetime
    end_dt: datetime
    status: MeetingStatus | None
    client_id: int | None


class MeetingsListResponse(BaseModel):
    own_meetings: conlist(MeetingResponse, min_items=0)
    other_client_meetings: conlist(MeetingResponse, min_items=0)