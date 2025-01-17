#!/bin/bash
set -e

# Load environment variables
source .env

# Build and push Docker image
echo "Building Docker image..."
docker build -t scraper:latest .
docker tag scraper:latest ${ECR_REPOSITORY_URI}:latest
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY_URI}
docker push ${ECR_REPOSITORY_URI}:latest

# Deploy infrastructure
echo "Deploying infrastructure..."
cd infrastructure
npm run build
npm run deploy -- --require-approval never

# Update ECS service
echo "Updating ECS service..."
aws ecs update-service --cluster scraper-cluster --service scraper-service --force-new-deployment

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
aws ecs wait services-stable --cluster scraper-cluster --services scraper-service

echo "Deployment completed successfully!"
