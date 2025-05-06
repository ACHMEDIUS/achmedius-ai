#!/bin/bash
# setup.sh
# Script to set up the project using PDM and create a .env file template

set -e

# Install PDM if not present
if ! command -v pdm &> /dev/null; then
    echo "PDM not found. Installing..."
    pip install pdm
fi

# Install dependencies
pdm install

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=" > .env
    echo ".env file created. Please add your OpenAI API key."
else
    echo ".env file already exists."
fi

echo "Setup complete."
