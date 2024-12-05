#!/usr/bin/env bash

echo "app Started ...."

cd /Users/gandhi/GandhiMain/700-Apps/watsonx-ai-util-app
python -m venv myvenv
source myvenv/bin/activate
python src/main.py

echo "app completed ...."