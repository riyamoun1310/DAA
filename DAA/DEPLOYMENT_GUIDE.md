# Deployment Guide for Riya Moun's Data Analyst Agent

This guide will help you deploy your personalized Data Analyst Agent on Render.

## 1. Prerequisites
- Python 3.8+
- A Google Generative AI API key
- A Render account

## 2. Environment Variables
Copy `.env.template` to `.env` and fill in your API key.

## 3. Deploy on Render
1. Push this repo to your GitHub account.
2. Go to [Render](https://render.com/), create a new Web Service, and connect your repo.
3. Set the build and start commands as per the `Procfile` and `Dockerfile`.
4. Add environment variables from your `.env` file.
5. Deploy!

## 4. Local Development
```sh
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

---
© 2025 Riya Moun
