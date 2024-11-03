import unittest
from src.blockchain.ledger import Ledger
from src.blockchain.consensus import Consensus
from src.blockchain.network import Network

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.consensus = Consensus()
        self.network = Network()

    def test_create_block(self):
        block_data = {"transactions": []}
        block = self.ledger.create_block(block_data)
        self.assertIsNotNone(block)
        self.assertEqual(block['index'], 1)  # Assuming this is the first block

    def test_validate_transaction(self):
        transaction = {"from": "Alice", "to": "Bob", "amount": 10}
        is_valid = self.ledger.validate_transaction(transaction)
        self.assertTrue(is_valid)

    def test_consensus_algorithm(self):
        result = self.consensus.run()
        self.assertIn(result, ["Proof of Work", "Proof of Stake"])  # Example consensus types

    def test_network_connection(self):
        self.network.connect("http://localhost:5000")
        self.assertTrue(self.network.is_connected())

if __name__ == "__main__":
    unittest.main()
