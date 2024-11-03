import unittest
from src.smart_contracts.utilities.utility_contract import UtilityContract

class TestUtilityContract(unittest.TestCase):
    def setUp(self):
        self.utility_contract = UtilityContract()

    def test_get_current_price(self):
        price = self.utility_contract.get_current_price("BTC")
        self.assertIsInstance(price, float)  # Assuming price is a float

    def test_convert_currency(self):
        amount = 100
        converted_amount = self.utility_contract.convert_currency(amount, "USD", "EUR")
        self.assertIsInstance(converted_amount, float)

if __name__ == "__main__":
    unittest.main()
