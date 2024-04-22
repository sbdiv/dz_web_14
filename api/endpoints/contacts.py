from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ..models.contact import Contact, ContactCreateUpdate
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import database
from models import schemas, contact
from .auth import oauth2_scheme
from jose import JWTError
import jwt

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Функція для отримання поточного користувача.

    Args:
        token (str): JWT токен.

    Returns:
        str: Електронна адреса поточного користувача.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Створює новий контакт у базі даних.

    Parameters:
        contact (schemas.ContactCreate): Об'єкт, що містить дані для створення контакту.
        db (Session, optional): Об'єкт сесії бази даних. За замовчуванням отримується залежність з функції `get_db`.
        current_user (str, optional): Email поточного користувача. За замовчуванням отримується залежність з функції `get_current_user`.

    Returns:
        schemas.Contact: Створений контакт.
    """
    return db.create_contact(contact)


@router.post("/contacts/")
def create_contact(contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    """
    Створити новий контакт.

    Parameters:
        contact (schemas.ContactCreate): Інформація про новий контакт.
        db (Session): Об'єкт сесії бази даних.
        current_user (str): Поточний користувач.

    Returns:
        schemas.Contact: Інформація про створений контакт.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Отримати список контактів.

    Parameters:
        skip (int): Кількість записів, які потрібно пропустити. За замовчуванням - 0.
        limit (int): Максимальна кількість записів, які потрібно повернути. За замовчуванням - 10.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        List[Contact]: Список контактів.
    """
    return db.query(Contact).offset(skip).limit(limit).all()

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Отримати інформацію про конкретний контакт.

    Parameters:
        contact_id (int): ID контакту.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        Contact: Інформація про контакт.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    """
    Оновити інформацію про контакт.

    Parameters:
        contact_id (int): ID контакту, який потрібно оновити.
        contact (ContactCreateUpdate): Інформація про контакт, яка потрібно оновити.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        Contact: Оновлена інформація про контакт.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact.dict().items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Видалити контакт.

    Parameters:
        contact_id (int): ID контакту, який потрібно видалити.
        db (Session): Об'єкт сесії бази даних.

    Returns:
        dict: Результат видалення.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}
