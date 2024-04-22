import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuthEndpoints(unittest.TestCase):

    def test_verify_email_success(self):
        email_data = {"email": "test@example.com", "verification_token": "123456"}
        response = client.post("/auth/verify_email", json=email_data)
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається повідомлення про успішну відправку листа
        self.assertEqual(response.json()["message"], "Email verification link has been sent")

    def test_verify_email_missing_data(self):

        email_data = {}
        response = client.post("/auth/verify_email", json=email_data)
        # Перевіряємо, чи повертається код відповіді 400 (помилка в запиті)
        self.assertEqual(response.status_code, 400)

    def test_login_for_access_token_success(self):
        # Надсилаємо POST-запит для отримання токену доступу з коректними даними
        login_data = {"username": "test@example.com", "password": "password123"}
        response = client.post("/auth/token", data=login_data)
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається токен доступу
        self.assertTrue("access_token" in response.json())

    def test_login_for_access_token_invalid_credentials(self):
        # Надсилаємо POST-запит для отримання токену доступу з неправильними даними
        login_data = {"username": "test@example.com", "password": "wrongpassword"}
        response = client.post("/auth/token", data=login_data)
        # Перевіряємо, чи повертається код відповіді 401 (неправильні облікові дані)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
