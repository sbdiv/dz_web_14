import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestContactsEndpoints(unittest.TestCase):

    def test_create_contact(self):
        # Надсилаємо POST-запит для створення контакту
        response = client.post(
            "/api/contacts/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "1234567890",
                "birthday": "1990-01-01"
            }
        )
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається коректний об'єкт контакту
        self.assertEqual(response.json()["first_name"], "John")
        self.assertEqual(response.json()["last_name"], "Doe")
    
    def test_read_contacts(self):
        response = client.get("/api/contacts/")
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається список контактів
        self.assertTrue(len(response.json()) > 0)
    
    def test_read_contact(self):
        response = client.get("/api/contacts/1")
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається коректний об'єкт контакту
        self.assertEqual(response.json()["id"], 1)
    
    def test_update_contact(self):
        # Надсилаємо PUT-запит для оновлення інформації про контакт
        response = client.put(
            "/api/contacts/1",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com",
                "phone_number": "9876543210",
                "birthday": "1990-01-01"
            }
        )
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи змінено атрибути контакту
        self.assertEqual(response.json()["first_name"], "Jane")
        self.assertEqual(response.json()["last_name"], "Doe")
    
    def test_delete_contact(self):
        # Надсилаємо DELETE-запит для видалення контакту
        response = client.delete("/api/contacts/1")
        # Перевіряємо, чи повертається код відповіді 200
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи повертається коректне повідомлення про видалення
        self.assertEqual(response.json()["message"], "Contact deleted")

if __name__ == '__main__':
    unittest.main()
