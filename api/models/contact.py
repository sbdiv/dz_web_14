from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date

Base = declarative_base()

class Contact(Base):
    """
    Модель для зберігання контактів.

    Attributes:
        id (int): Унікальний ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Електронна адреса контакту.
        phone_number (str): Номер телефону контакту.
        birthday (date): Дата народження контакту.
        additional_data (str, optional): Додаткова інформація про контакт (необов'язково).
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)

class ContactCreateUpdate(BaseModel):
    """
    Модель для створення або оновлення контакту.

    Attributes:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Електронна адреса контакту.
        phone_number (str): Номер телефону контакту.
        birthday (date): Дата народження контакту.
        additional_data (str, optional): Додаткова інформація про контакт (необов'язково).
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None
