from fastapi import FastAPI, APIRouter
from api.endpoints import contacts, birthdays, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
api_router = APIRouter()

app.include_router(contacts.router, prefix="/api")
app.include_router(birthdays.router, prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(birthdays.router, prefix="/birthdays", tags=["birthdays"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)