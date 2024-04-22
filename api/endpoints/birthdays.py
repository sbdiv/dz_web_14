from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ...database.database import get_db
from ..models.contact import Contact
from sqlalchemy.sql.functions import extract

router = APIRouter()

@router.get("/contacts/birthday", response_model=List[Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    """
    Отримує список контактів з наступними днями народження.

    Parameters:
        db (Session): Об'єкт сесії бази даних.

    Returns:
        List[Contact]: Список контактів, у яких день народження настає протягом наступних 7 днів.
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= end_date.day
    ).all()

