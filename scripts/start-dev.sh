#!/bin/bash

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run populate-env-variables.sh to ensure .env exists
"$SCRIPT_DIR/populate-env-variables.sh"
POPULATE_EXIT_CODE=$?

# If populate script exited with code 2 (waiting for user to edit .env), stop here
if [ $POPULATE_EXIT_CODE -eq 2 ]; then
    exit 0
fi

# If populate script failed, exit with error
if [ $POPULATE_EXIT_CODE -ne 0 ]; then
    echo "❌ Failed to populate environment variables"
    exit 1
fi

# Enable Docker BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

echo "🚀 Starting hispanie backend development..."
echo "   ✅ Docker BuildKit enabled"
echo ""

# Build and start services
echo "🐳 Building and starting services..."
docker-compose up -d --build

echo ""
echo "✅ Development environment ready!"
echo ""
echo "🌐 Services:"
echo "   API:      http://localhost:3201"
echo "   Database: localhost:5432"
echo ""
echo "📝 Commands:"
echo "   Logs: docker-compose logs -f"
echo "   Stop: docker-compose down"
