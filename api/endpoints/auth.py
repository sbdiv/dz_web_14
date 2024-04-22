from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models import schemas,mail
from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
import os

router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")\
    



conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = int(os.getenv("MAIL_PORT")),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_TLS = True if os.getenv("MAIL_TLS").lower() == "true" else False,
    MAIL_SSL = True if os.getenv("MAIL_SSL").lower() == "true" else False,
    TEMPLATE_FOLDER = "./api/templates"
)

@router.post("/verify_email")
async def verify_email(email_verification: schemas.EmailVerification):
    """
    Відправляє листа для верифікації електронної пошти зареєстрованого користувача.

    Parameters:
        email_verification (schemas.EmailVerification): Об'єкт, який містить адресу електронної пошти
        користувача та токен верифікації.

    Returns:
        dict: Результат операції.

    Raises:
        HTTPException: Якщо не вказано адресу електронної пошти або токен верифікації.

    """
    if not email_verification.email:
        raise HTTPException(status_code=400, detail="Email is required")

    if not email_verification.verification_token:
        raise HTTPException(status_code=400, detail="Verification token is required")

    message = MessageSchema(
        subject="Email Verification",
        recipients=[email_verification.email],
        body=f"Click the link to verify your email: https://example.com/verify_email?token={email_verification.verification_token}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    
    return {"message": "Email verification link has been sent"}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(schemas.User).filter(schemas.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
