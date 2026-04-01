#!/bin/bash

filenames=(
  ".dockerignore" 
  ".env" 
  "api.py" 
  "Dockerfile" 
  "requirements.txt" 
  "README.md" 
  "server.py" 
  "services.py" 
  "server_stream.py" 
  "client_test.py"
  )

for filename in "${filenames[@]}"; do
  touch "$filename"
done