import unittest
from src.blockchain.ledger import Ledger

class TestLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()

    def test_add_transaction(self):
        transaction = {"from": "Alice", "to": "Bob", "amount": 10}
        self.ledger.add_transaction(transaction)
        self.assertIn(transaction, self.ledger.pending_transactions)

    def test_commit_transactions(self):
        transaction1 = {"from": "Alice", "to": "Bob", "amount": 10}
        transaction2 = {"from": "Bob", "to": "Charlie", "amount": 5}
        self.ledger.add_transaction(transaction1)
        self.ledger.add_transaction(transaction2)
        self.ledger.commit_transactions()
        self.assertEqual(len(self.ledger.pending_transactions), 0)
        self.assertEqual(len(self.ledger.chain), 1)  # Assuming one block is created

if __name__ == "__main__":
    unittest.main()
