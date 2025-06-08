# AI Email Agent

## Overview
This AI Email Agent automatically replies to emails, excluding those related to quotations, and sends a daily summary report. It is designed to run on Render.com.

## Setup and Deployment

### Step 1: Create a GitHub Repository
1. Create a new GitHub repository (e.g., `ai-email-agent`).
2. Add the `ai_email_agent.py` script to the repository.
3. Add the `requirements.txt` file to the repository.

### Step 2: Add Environment Variables on Render.com
1. Sign up for an account on Render.com.
2. Create a new **Background Worker** service.
3. Connect it to your GitHub repository.
4. Add the following environment variables:
   - `EMAIL_ADDRESS` = `business@camuh.com.ng`
   - `EMAIL_PASSWORD` = your secure password or app password

### Step 3: Set Up the Background Worker
1. Set the start command to:
   python ai_email_agent.py

### Step 4: Deploy and Run
1. Deploy the service.
2. Monitor logs to ensure the agent is running correctly.
3. Check your email for daily summary reports.

## Security Note
Ensure your email password is stored securely as an environment variable and not hard-coded in the script.
