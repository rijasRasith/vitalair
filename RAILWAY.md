# VitalAir - Railway Deployment Guide

This document provides instructions for deploying the VitalAir application on Railway.app.

## Prerequisites

- A Railway.app account
- GitHub account with your code repository

## Steps to Deploy

1. **Create a Railway account** (if you don't already have one)
   - Go to [Railway.app](https://railway.app/)
   - Sign up with GitHub

2. **Create a new project in Railway**
   - Click on "New Project"
   - Select "Deploy from GitHub repo"
   - Select your VitalAir repository

3. **Configure Environment Variables**
   - In your Railway project, go to the "Variables" tab
   - Add the following variables:
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
     - Any other environment variables your app needs

4. **Deployment Settings**
   - Railway will automatically detect the Procfile and railway.toml configuration
   - The app will be deployed on the port provided by Railway (via the $PORT variable)

5. **Monitor the deployment**
   - Check the "Deployments" tab to see the build and deployment logs
   - Once complete, your app will be available at the provided Railway URL

## Common Issues

- **If the app fails to start**: Check the logs for any errors
- **If the Telegram bot doesn't work**: Make sure the TELEGRAM_BOT_TOKEN environment variable is correctly set
- **If you see port binding errors**: Make sure the app is using $PORT from the environment

## Maintaining Your Deployment

- **Update the application**: Push changes to your GitHub repo, and Railway will automatically redeploy
- **Scale the application**: Railway allows you to adjust resources as needed in their dashboard
- **Monitor usage**: Keep an eye on your Railway dashboard to track usage against your free tier limits

## Contact

If you need further assistance with deployment, please contact the VitalAir team. 