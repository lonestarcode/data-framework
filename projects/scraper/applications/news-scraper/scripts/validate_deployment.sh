#!/bin/bash
set -e

# Check ECS service status
echo "Checking ECS service status..."
SERVICE_STATUS=$(aws ecs describe-services --cluster scraper-cluster --services scraper-service --query 'services[0].status' --output text)

if [ "$SERVICE_STATUS" != "ACTIVE" ]; then
    echo "Service is not active. Status: $SERVICE_STATUS"
    exit 1
fi

# Check database connectivity
echo "Checking database connectivity..."
python -c "
from src.database.models import Base
from sqlalchemy import create_engine
engine = create_engine('${DATABASE_URL}')
Base.metadata.create_all(engine)
"

# Check Redis connectivity
echo "Checking Redis connectivity..."
redis-cli -h ${REDIS_HOST} ping

# Check metrics endpoint
echo "Checking metrics endpoint..."
curl -f http://localhost:8000/metrics

echo "All validation checks passed!" 