# src/blockchain/ledger/ledger.py

import hashlib
import json
import logging
from time import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time()

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

class Block:
    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Ledger:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1')  # Genesis block

    def create_block(self, previous_hash):
        block = Block(index=len(self.chain) + 1, previous_hash=previous_hash, transactions=self.current_transactions)
        self.current_transactions = []  # Reset the current transactions
        self.chain.append(block)
        logging.info(f"Block {block.index} created with hash: {block.hash}")
        return block

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        logging.info(f"Transaction added: {transaction.to_json()}")
        return self.last_block.index + 1  # Return the index of the block that will hold this transaction

    @property
    def last_block(self):
        return self.chain[-1]

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if the hash of the block is correct
            if current.hash != current.calculate_hash():
                logging.error(f"Invalid block hash at index {i}")
                return False

            # Check if the previous hash is correct
            if current.previous_hash != previous.hash:
                logging.error(f"Invalid previous hash at index {i}")
                return False

        logging.info("Blockchain is valid.")
        return True

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.get_chain(), f)
            logging.info(f"Ledger saved to {filename}")

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            chain_data = json.load(f)
            self.chain = [Block(**block) for block in chain_data]
            logging.info(f"Ledger loaded from {filename}")

# Example usage
if __name__ == "__main__":
    ledger = Ledger()
    
    # Adding transactions
    ledger.add_transaction("Alice", "Bob", 50)
    ledger.add_transaction("Bob", "Charlie", 30)

    # Creating a new block
    ledger.create_block(previous_hash=ledger.last_block.hash)

    # Validating the blockchain
    ledger.validate_chain()

    # Saving the ledger to a file
    ledger.save_to_file("ledger.json")

    # Loading the ledger from a file
    new_ledger = Ledger()
    new_ledger.load_from_file("ledger.json")
    new_ledger.validate_chain()
