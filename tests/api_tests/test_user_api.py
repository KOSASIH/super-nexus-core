import unittest
import requests

class TestUser API(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api/v1/users"

    def test_register_user(self):
        user_data = {"username": "Alice", "password": "securepassword"}
        response = requests.post(f"{self.BASE_URL}/register", json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json())

    def test_login_user(self):
        user_data = {"username": "Alice", "password": "securepassword"}
        response = requests.post(f"{self.BASE_URL}/login", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_invalid_user(self):
        user_data = {"username": "Alice", "password": "wrongpassword"}
        response = requests.post(f"{self.BASE_URL}/login", json=user_data)
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
