import unittest
from src.blockchain.network import Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.network = Network()

    def test_add_peer(self):
        self.network.add_peer("http://localhost:5001")
        self.assertIn("http://localhost:5001", self.network.peers)

    def test_remove_peer(self):
        self.network.add_peer("http://localhost:5001")
        self.network.remove_peer("http://localhost:5001")
        self.assertNotIn("http://localhost:5001", self.network.peers)

    def test_broadcast_message(self):
        self.network.add_peer("http://localhost:5001")
        message = {"type": "new_block", "data": "block_data"}
        response = self.network.broadcast(message)
        self.assertTrue(response)  # Assuming broadcast returns True on success

if __name__ == "__main__":
    unittest.main()
