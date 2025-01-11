#!/bin/bash

# Set your project ID and instance name
export PROJECT_ID=your-project-id
export INSTANCE_NAME=your-instance-name

# Create a Cloud SQL instance
gcloud sql instances create $INSTANCE_NAME --project=$PROJECT_ID --database-version=MYSQL_5_7 --tier=db-n1-standard-1 --region=us-central1

# Get the INSTANCE_CONNECTION_NAME for the Cloud SQL instance
export INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format='value(connectionName)')

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/my-app .

# Push the Docker image to Google Container Registry
docker push gcr.io/$PROJECT_ID/my-app

# Deploy the image to Cloud Run, passing the INSTANCE_CONNECTION_NAME as an environment variable
gcloud run deploy my-app --image gcr.io/$PROJECT_ID/my-app --add-cloudsql-instances $INSTANCE_CONNECTION_NAME --update-env-vars INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME --region us-central1 --platform managed