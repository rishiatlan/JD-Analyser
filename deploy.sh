#!/bin/bash

# Frontend Deployment to Vercel
echo "Deploying frontend to Vercel..."
cd frontend
vercel --prod

# Backend Deployment to AWS Elastic Beanstalk
echo "Deploying backend to AWS Elastic Beanstalk..."
cd ..
eb deploy jd-analyzer-prod

echo "Deployment complete!" 