#!/bin/bash

# Script to create .env from template and populate environment variables

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

ENV_TEMPLATE="$PROJECT_ROOT/.env.template"
ENV_FILE="$PROJECT_ROOT/.env"

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file from template..."

    if [ ! -f "$ENV_TEMPLATE" ]; then
        echo "Error: .env.template not found at $ENV_TEMPLATE"
        exit 1
    fi

    cp "$ENV_TEMPLATE" "$ENV_FILE"

    echo ""
    echo "✅ .env file created at $ENV_FILE"
    echo ""
    echo "⚠️  Please edit the .env file and fill in your values, then run this script again."
    echo ""
    exit 0
fi

# .env exists, populate variables
echo "Loading environment variables from .env..."

# Create a marker for Hispanie Backend section in .bashrc
MARKER_START="# >>> Hispanie Backend Environment Variables >>>"
MARKER_END="# <<< Hispanie Backend Environment Variables <<<"

# Check if marker exists in .bashrc
if ! grep -q "$MARKER_START" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "$MARKER_START" >> ~/.bashrc
    echo "$MARKER_END" >> ~/.bashrc
    echo "Created Hispanie Backend section in ~/.bashrc"
fi

# Read variables and export them
while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue

    # Export for current session
    export "$line"

    # Extract variable name
    var_name=$(echo "$line" | cut -d'=' -f1)

    # Check if variable already exists in the Hispanie Backend section
    if ! sed -n "/$MARKER_START/,/$MARKER_END/p" ~/.bashrc | grep -q "^export $var_name="; then
        # Add to .bashrc in the Hispanie Backend section
        sed -i "/$MARKER_END/i export $line" ~/.bashrc
    fi
done < "$ENV_FILE"

echo "✅ Environment variables populated"
echo "✅ Variables saved to ~/.bashrc (Hispanie Backend section)"
echo ""
echo "Run 'source ~/.bashrc' in other terminals to load them"
