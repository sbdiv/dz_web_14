import requests
import pytest

@pytest.fixture(scope="module")
def start_server():
    from main import app
    import uvicorn
    import threading

    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000)

    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    yield
    server_thread.join()

# Функція, яка перевіряє, чи повертає маршрут /api/contacts/ правильні дані
def test_get_contacts(start_server):
    response = requests.get("http://127.0.0.1:8000/api/contacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Функція, яка перевіряє, чи повертає маршрут /api/contacts/{contact_id} правильний контакт
def test_get_contact_by_id(start_server):
    contact_id = 1
    response = requests.get(f"http://127.0.0.1:8000/api/contacts/{contact_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Функція, яка перевіряє, чи повертає маршрут /api/contacts/birthday правильні дані
def test_get_upcoming_birthdays(start_server):
    response = requests.get("http://127.0.0.1:8000/api/contacts/birthday")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
# Функція, яка перевіряє, чи повертає маршрут /auth/token правильний токен доступу
def test_get_access_token(start_server):
    data = {
        "username": "your_username",
        "password": "your_password"
    }
    response = requests.post("http://127.0.0.1:8000/auth/token", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
