#!/bin/bash

# Upgrade pip in the virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install Flask, Hugging Face Transformers, and PyTorch
echo "Installing Flask, transformers, and PyTorch..."
pip install Flask transformers torch

# Install the necessary model dependencies
echo "Installing model dependencies..."
pip install sentencepiece

echo "Installation complete. You can now run the Flask server."

