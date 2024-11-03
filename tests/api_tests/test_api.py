import unittest
import requests

class TestAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api/v1"

    def test_get_balance(self):
        response = requests.get(f"{self.BASE_URL}/balance?address=Alice")
        self.assertEqual(response.status_code, 200)
        self.assertIn("balance", response.json())

    def test_post_transaction(self):
        transaction_data = {"from": "Alice", "to": "Bob", "amount": 10}
        response = requests.post(f"{self.BASE_URL}/transaction", json=transaction_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("transaction_id", response.json())

    def test_invalid_endpoint(self):
        response = requests.get(f"{self.BASE_URL}/invalid")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
