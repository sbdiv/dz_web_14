from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timedelta

app = FastAPI()

requests = {}

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware для обмеження швидкості запитів.

    Parameters:
        request (Request): Об'єкт запиту.
        call_next: Функція для виклику наступного middleware.

    Returns:
        Response: Відповідь на запит.
    """
    ip = request.client.host
    now = datetime.now()

    if ip in requests:
        requests[ip] = [req for req in requests[ip] if now - req < timedelta(minutes=1)]
        if len(requests[ip]) >= 5:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    else:
        requests[ip] = []

    requests[ip].append(now)

    response = await call_next(request)
    return response
