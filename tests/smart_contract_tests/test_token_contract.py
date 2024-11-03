import unittest
from src.smart_contracts.token.token_contract import TokenContract

class TestTokenContract(unittest.TestCase):
    def setUp(self):
        self.token_contract = TokenContract()
        self.token_contract.mint("Alice", 100)

    def test_initial_balance(self):
        balance = self.token_contract.get_balance("Alice")
        self.assertEqual(balance, 100)

    def test_transfer_tokens(self):
        self.token_contract.transfer("Alice", "Bob", 50)
        balance_alice = self.token_contract.get_balance("Alice")
        balance_bob = self.token_contract.get_balance("Bob")
        self.assertEqual(balance_alice, 50)
        self.assertEqual(balance_bob, 50)

    def test_transfer_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.token_contract.transfer("Alice", "Bob", 100)

if __name__ == "__main__":
    unittest.main()
