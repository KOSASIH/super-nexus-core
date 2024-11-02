# src/blockchain/network/p2p.py

import socket
import threading
import json
import logging
import time
import hashlib
import os
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class P2PNode:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.nodes = set()  # Set of connected nodes
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        logging.info(f"Listening for connections on {self.host}:{self.port}")

        while True:
            client_socket, address = server_socket.accept()
            logging.info(f"Connection from {address} has been established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.process_message(json.loads(message))
            except Exception as e:
                logging.error(f"Error handling client: {e}")
                break
        client_socket.close()

    def process_message(self, message):
        message_type = message.get('type')
        if message_type == 'transaction':
            self.handle_transaction(message['data'])
        elif message_type == 'block':
            self.handle_block(message['data'])
        elif message_type == 'nodes':
            self.handle_nodes(message['data'])
        elif message_type == 'ping':
            self.send_pong(message['data'])
        elif message_type == 'pong':
            logging.info(f"Received pong from {message['data']}")

    def handle_transaction(self, transaction):
        logging.info(f"Received transaction: {transaction}")
        # Here you would add logic to validate and add the transaction to the local ledger

    def handle_block(self, block):
        logging.info(f"Received block: {block}")
        # Here you would add logic to validate and add the block to the local blockchain

    def handle_nodes(self, nodes):
        logging.info(f"Received nodes: {nodes}")
        self.nodes.update(nodes)

    def send_pong(self, sender):
        message = {
            'type': 'pong',
            'data': (self.host, self.port)
        }
        self.send_message(sender, message)

    def connect_to_node(self, node_address):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(node_address)
            self.nodes.add(node_address)
            logging.info(f"Connected to node: {node_address}")
            self.send_nodes(client_socket)
            client_socket.close()
        except Exception as e:
            logging.error(f"Could not connect to node {node_address}: {e}")

    def send_nodes(self, client_socket):
        message = {
            'type': 'nodes',
            'data': list(self.nodes)
        }
        client_socket.send(json.dumps(message).encode('utf-8'))

    def broadcast_transaction(self, transaction):
        message = {
            'type': 'transaction',
            'data': transaction
        }
        self.broadcast(message)

    def broadcast_block(self, block):
        message = {
            'type': 'block',
            'data': block
        }
        self.broadcast(message)

    def broadcast(self, message):
        for node in self.nodes:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(node)
                client_socket.send(json.dumps(message).encode('utf-8'))
                client_socket.close()
            except Exception as e:
                logging.error(f"Error broadcasting to {node}: {e}")

    def discover_nodes(self):
        # This method could implement a more sophisticated discovery mechanism
        # For now, it just logs the current known nodes
        logging.info(f"Known nodes: {self.nodes}")

     def ping_nodes(self):
        for node in self.nodes:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(1)  # Set a timeout for the connection
                client_socket.connect(node)
                message = {
                    'type': 'ping',
                    'data': (self.host, self.port)
                }
                client_socket.send(json.dumps(message).encode('utf-8'))
                client_socket.close()
            except Exception as e:
                logging.error(f"Node {node} is unreachable: {e}")
                self.nodes.remove(node)  # Remove unreachable nodes

    def send_message(self, recipient, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(recipient)
            client_socket.send(json.dumps(message).encode('utf-8'))
            client_socket.close()
        except Exception as e:
            logging.error(f"Error sending message to {recipient}: {e}")

    def sign_message(self, message, private_key):
        # Here you would implement a signing mechanism using a cryptographic library
        # For demonstration, we'll just return a dummy signature
        return hashlib.sha256(json.dumps(message).encode('utf-8')).hexdigest()

    def verify_signature(self, message, signature):
        # Here you would implement a verification mechanism
        # For demonstration, we'll just check if the signature matches
        expected_signature = self.sign_message(message, private_key=None)  # Replace with actual private key
        return expected_signature == signature

    def hash_data(self, data):
        return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()

# Example usage
if __name__ == "__main__":
    node = P2PNode()

    # Simulate connecting to another node
    time.sleep(2)  # Wait for the server to start
    node.connect_to_node(('localhost', 5001))

    # Periodically ping nodes to check their availability
    while True:
        node.ping_nodes()
        time.sleep(10)  # Ping every 10 seconds
