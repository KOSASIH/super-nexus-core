# src/blockchain/network/node.py

import time
import json
import hashlib
import logging
from blockchain.network.p2p import P2PNode

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')  # Create the genesis block

    def create_block(self, data):
        index = len(self.chain) + 1
        previous_hash = self.chain[-1].hash if self.chain else '0'
        timestamp = time.time()
        hash = self.hash_block(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(block)
        return block

    def hash_block(self, index, previous_hash, timestamp, data):
        block_string = json.dumps({
            'index': index,
            'previous_hash': previous_hash,
            'timestamp': timestamp,
            'data': data
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Node:
    def __init__(self, host='localhost', port=5000):
        self.p2p_node = P2PNode(host, port)
        self.blockchain = Blockchain()

    def create_transaction(self, data):
        # Here you would add logic to create a transaction
        transaction = {
            'data': data,
            'timestamp': time.time()
        }
        logging.info(f"Creating transaction: {transaction}")
        self.broadcast_transaction(transaction)

    def broadcast_transaction(self, transaction):
        self.p2p_node.broadcast_transaction(transaction)

    def create_block(self, data):
        block = self.blockchain.create_block(data)
        logging.info(f"New block created: {block.to_dict()}")
        self.broadcast_block(block)

    def broadcast_block(self, block):
        self.p2p_node.broadcast_block(block.to_dict())

# Example usage
if __name__ == "__main__":
    node = Node()

    # Simulate creating a transaction
    node.create_transaction("User  A sends 5 coins to User B")

    # Simulate creating a block
    node.create_block("Block data for the new block")

    # Keep the node running
    while True:
        time.sleep(10)  # Keep the node alive
