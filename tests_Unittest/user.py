import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestUserEndpoints(unittest.TestCase):

    def test_upload_avatar(self):
        # Надсилаємо POST-запит для завантаження аватара
        with open("test_avatar.png", "rb") as file:
            response = client.post("/api/upload_avatar/", files={"file": file})
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається URL аватара
        self.assertTrue("avatar_url" in response.json())

if __name__ == '__main__':
    unittest.main()
