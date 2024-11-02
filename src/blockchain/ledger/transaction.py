# src/blockchain/ledger/transaction.py

import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.transaction_id = self.generate_transaction_id()

    def generate_transaction_id(self):
        # Generate a unique transaction ID (could be improved with a more robust method)
        return f"{self.sender}-{self.recipient}-{self.amount}-{self.timestamp}"

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        transaction = Transaction(data['sender'], data['recipient'], data['amount'])
        transaction.timestamp = data['timestamp']
        transaction.transaction_id = data['transaction_id']
        return transaction

    def validate(self):
        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            logging.error("Invalid transaction amount.")
            return False
        if not self.sender or not self.recipient:
            logging.error("Sender and recipient must be specified.")
            return False
        logging.info("Transaction is valid.")
        return True

# Example usage
if __name__ == "__main__":
    # Create a transaction
    transaction = Transaction("Alice", "Bob", 50)

    # Validate the transaction
    if transaction.validate():
        logging.info(f"Transaction created: {transaction.to_json()}")

    # Serialize to JSON
    json_transaction = transaction.to_json()
    logging.info(f"Serialized transaction: {json_transaction}")

    # Deserialize from JSON
    new_transaction = Transaction.from_json(json_transaction)
    logging.info(f"Deserialized transaction: {new_transaction.to_json()}")
