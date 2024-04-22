import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestBirthdaysEndpoints(unittest.TestCase):

    def test_get_upcoming_birthdays_endpoint(self):
        response = client.get("/api/contacts/birthday")
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи список народжень не пустий
        self.assertTrue(len(response.json()) > 0)
    
    def test_get_upcoming_birthdays_no_contacts(self):
        response = client.get("/api/contacts/birthday")
        self.assertEqual(response.status_code, 404)
    
    def test_get_upcoming_birthdays_invalid_date(self):
        # Надсилаємо запит з недійсною датою
        response = client.get("/api/contacts/birthday?date=2023-13-40")
        # Очікуємо отримати помилку з кодом 422 (неприпустима дата)
        self.assertEqual(response.status_code, 422)
    
    def test_get_upcoming_birthdays_invalid_date_format(self):
        # Надсилаємо запит з неправильним форматом дати
        response = client.get("/api/contacts/birthday?date=2023-02-40")
        # Очікуємо отримати помилку з кодом 422 (неприпустимий формат дати)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
