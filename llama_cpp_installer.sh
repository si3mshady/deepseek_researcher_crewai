#!/bin/bash

# Update system and install essential dependencies
echo "Updating system and installing essential dependencies..."
sudo apt update
sudo apt install -y git cmake g++ python3-dev python3-pip build-essential

# Clone the Llama.cpp repository
echo "Cloning Llama.cpp repository..."
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Create a build directory and run cmake
echo "Building Llama.cpp..."
mkdir build
cd build
cmake ..
make -j$(nproc)  # Adjust the number of cores based on your machine (e.g., -j4)

# Optionally, install Python bindings if you want to use Llama.cpp in Python
echo "Installing Python bindings..."
cd ..
pip install -r requirements.txt  # Install necessary Python dependencies

# Test Llama.cpp (just to verify that everything is working)
echo "Testing Llama.cpp..."
./build/bin/llama --help  # This will print help text if everything is working

# Define paths for Llama.cpp and the model
LLAMA_CPP_PATH="$(pwd)/llama.cpp"
MODEL_PATH="$(pwd)/models/quantized_model.bin"  # Adjust this path if your model is in a different directory

# Output the paths to the user for configuration
echo "Llama.cpp is located at: $LLAMA_CPP_PATH"
echo "Quantized model file is expected at: $MODEL_PATH"

# Output where you should put the model (if the model is not downloaded yet)
echo "Please make sure your quantized model file (quantized_model.bin) is located at the path above. If it's not, download or place the model in this directory."

echo "Llama.cpp installation complete. You can now use the following paths in your Flask app:"
echo "LLAMA_CPP_PATH = \"$LLAMA_CPP_PATH\""
echo "MODEL_PATH = \"$MODEL_PATH\""


