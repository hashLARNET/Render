#!/bin/bash
echo "Starting FastAPI application from backend folder..."
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
