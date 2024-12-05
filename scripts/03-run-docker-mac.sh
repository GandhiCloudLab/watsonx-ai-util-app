#!/usr/bin/env bash

echo "docker run Started ...."

DOCKER_IMAGE=gandigit/watsonx-ai-util-app

echo "Hope this is valid .... WATSONX_API_KEY --> $WATSONX_API_KEY"

podman run -d -p 3001:3001 --name watsonx-ai-util-app \
    --env LOGLEVEL=DEBUG \
    --env WATSONX_API_KEY=$WATSONX_API_KEY \
    gandigit/watsonx-ai-util-app:latest

echo "run completed ...."