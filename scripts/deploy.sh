#!/bin/bash

# deploy.sh - Deployment script for the blockchain application

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
CONTRACT_DIR="./src/smart_contracts"
DEPLOYMENT_DIR="./deployments"
NETWORK="testnet"  # Change to mainnet for production
NODE_URL="http://localhost:8545"  # URL of the blockchain node

# Function to deploy smart contracts
deploy_contracts() {
    echo "Deploying smart contracts..."
    for contract in $(ls $CONTRACT_DIR/*.sol); do
        echo "Deploying contract: $contract"
        # Assuming you have a tool like Truffle or Hardhat for deployment
        npx hardhat run $contract --network $NETWORK
    done
    echo "Smart contracts deployed successfully."
}

# Function to start services
start_services() {
    echo "Starting necessary services..."
    # Start your blockchain node, API server, etc.
    nohup npm start &  # Start the API server in the background
    echo "Services started."
}

# Main script execution
echo "Starting deployment process..."
deploy_contracts
start_services
echo "Deployment completed successfully."
