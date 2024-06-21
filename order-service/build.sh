#! /bin/bash

docker login
# Build an image an push an image into the Docker Hub
docker build --tag pythonplant12/order:v1.0.0 -f Dockerfile .
docker push pythonplant12/order:v1.0.0