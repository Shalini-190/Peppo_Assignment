# Peppo AI — Text-to-Video Generation Web App

A minimal AI-integrated web application demonstrating an end-to-end pipeline for text-to-video generation. Built as part of the Peppo AI Engineering Internship Technical Challenge.

## Overview

The app takes a user prompt via text input, sends it to a Flask backend, and returns a generated video. Due to the cost and latency of free text-to-video APIs, the project uses a placeholder demo video with a production-ready architecture that can integrate with Runway, Pika Labs, or Stability AI.

## Features

- **Prompt Input** — Clean web interface for entering video descriptions
- **Flask Backend** — Python server handling request processing
- **Mock Video Pipeline** — Placeholder demo simulating real API integration
- **Logging System** — Shows how the system interacts with a real video generation API
- **Cloud-Ready** — Deployable to Render, Railway, Vercel, or any cloud provider

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Deployment:** Render-compatible

## Getting Started

```bash
git clone https://github.com/Shalini-190/Peppo_Assignment.git
cd Peppo_Assignment
pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:5000` in your browser.

## Project Structure

```
├── main.py              # Flask API server
├── templates/           # HTML frontend
├── static/              # Static assets
├── requirements.txt     # Dependencies
└── README.md
```

## Production Plan

- Integrate Runway or Pika Labs API
- Add async job queues (Celery/Redis) for long-running renders
- Implement caching for repeated prompts
- Add user feedback ("Your video is being processed")

## License

MIT
