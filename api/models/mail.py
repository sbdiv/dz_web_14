from pydantic import BaseModel


class EmailVerification(BaseModel):
    """
    Модель для електронного підтвердження.

    Attributes:
        email (str): Електронна адреса користувача.
        verification_token (str): Токен для підтвердження електронної пошти.
    """
    email: str
    verification_token: str