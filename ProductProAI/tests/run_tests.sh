#!/bin/bash

# Run all tests for ProductPro AI
echo "Running ProductPro AI test suite..."

# Change to the project directory
cd "$(dirname "$0")/.."

# Run API tests
echo "Running API tests..."
python3 -m tests.test_api

# Run image recognition tests
echo "Running image recognition tests..."
python3 -m tests.test_image_recognition

# Run NLP tests
echo "Running NLP tests..."
python3 -m tests.test_nlp

# Run design engine tests
echo "Running design engine tests..."
python3 -m tests.test_design_engine

echo "All tests completed!"
