from os import environ

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from schemas.meeting import Meeting

conf = ConnectionConfig(
    MAIL_FROM=environ.get('EMAIL_FROM_NAME'),
    MAIL_USERNAME=environ.get('EMAIL_HOST_USER'),
    MAIL_PASSWORD=environ.get('EMAIL_HOST_PASSWORD'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False
)


async def send_in_background(
    background_tasks: BackgroundTasks,
    email: str,
    meeting_data: Meeting,
    ):

    message = MessageSchema(
        subject="Booking meeting on John course",
        recipients=[email,],
        body=f"""Your meeting '{meeting_data.title}' at 
             '{meeting_data.start_dt.strftime("%m/%d/%Y, %H:%M:%S")}'
             successfully {meeting_data.status}
             """,
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return "Sended"