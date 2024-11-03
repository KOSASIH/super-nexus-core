#!/bin/bash

# migrate.sh - Database migration script for the blockchain application

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
MIGRATION_DIR="./migrations"
DATABASE_URL="your_database_url"  # Replace with your actual database URL

# Function to run migrations
run_migrations() {
    echo "Running database migrations..."
    # Assuming you are using a migration tool like Knex.js or Sequelize
    npx knex migrate:latest --knexfile $MIGRATION_DIR/knexfile.js --env development
    echo "Database migrations completed successfully."
}

# Main script execution
echo "Starting migration process..."
run_migrations
