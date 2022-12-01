from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import meeting, user
from routers.login import router as login_router
from routers.meeting import router as meeting_router
from routers.signup import router as signup_router
from db import engine

user.Base.metadata.create_all(bind=engine)
meeting.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(login_router)
app.include_router(meeting_router)
app.include_router(signup_router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
