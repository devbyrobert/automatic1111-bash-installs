#!/bin/bash

echo "Step 1: Installing required packages..."
sudo apt install -y wget git python3 python3-venv > /dev/null 2>&1

echo "Step 2: Cloning stable-diffusion-webui repository..."
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git > /dev/null 2>&1

echo "Step 3: Changing directory to stable-diffusion-webui..."
cd stable-diffusion-webui

echo "Step 4: Downloading model to stable-diffusion-webui/models/Stable-diffusion..."
wget -q -O models/Inkpunk-Diffusion-v2.ckpt https://huggingface.co/Envvi/Inkpunk-Diffusion/resolve/main/Inkpunk-Diffusion-v2.ckpt

echo "Step 5: Installing opencv-python package..."
pip install opencv-python > /dev/null 2>&1

echo "Step 6: Installing additional extensions..."
git clone https://github.com/LonicaMewinsky/gif2gif.git extensions/gif2gif > /dev/null 2>&1

echo "Step 7: Installing mesa-utils..."
sudo apt-get install -y mesa-utils > /dev/null 2>&1

echo "Step 8: Running webui.sh script..."
bash webui.sh -f --share --xformers --enable-insecure-extension-access