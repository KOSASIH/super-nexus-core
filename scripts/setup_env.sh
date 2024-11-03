#!/bin/bash

# setup_env.sh - Environment setup script for the blockchain application

set -e  # Exit immediately if a command exits with a non-zero status

# Function to install Node.js and npm
install_node() {
    echo "Installing Node.js and npm..."
    if ! command -v node &> /dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
        sudo apt-get install -y nodejs
    else
        echo "Node.js is already installed."
    fi
}

# Function to install project dependencies
install_dependencies() {
    echo "Installing project dependencies..."
    npm install
}

# Function to set up environment variables
setup_env_variables() {
    echo "Setting up environment variables..."
    echo "NODE_ENV=development" >> .env
    echo "DATABASE_URL=your_database_url" >> .env
    echo "BLOCKCHAIN_NODE_URL=http://localhost:8545" >> .env
}

# Main script execution
echo "Starting environment setup..."
install_node
install_dependencies
setup_env_variables
echo "Environment setup completed successfully."
