#!/bin/bash
# Web Guardian Setup & Run Script

PROJECT_DIR="/home/jinhan2/opencode_project/web_guardian"
cd $PROJECT_DIR

echo "🚀 [1/3] Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 [2/3] Installing Playwright Chromium binary..."
playwright install chromium

echo "🏃 [3/3] Running Web Guardian..."
python3 main.py
