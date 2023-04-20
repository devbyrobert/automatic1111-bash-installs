#!/bin/bash

echo "Step 1: Installing required packages..."
sudo apt install -y wget git python3 python3-venv > /dev/null 2>&1

echo "Step 2: Cloning stable-diffusion-webui repository..."
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git > /dev/null 2>&1

echo "Step 3: Changing directory to stable-diffusion-webui..."
cd stable-diffusion-webui

echo "Step 4: Downloading model to stable-diffusion-webui/models/Stable-diffusion..."
wget -q -O models/Realistic_Vision.ckpt https://huggingface.co/SG161222/Realistic_Vision_V2.0/resolve/main/Realistic_Vision_V2.0.ckpt

echo "Step 5: Installing text-to-video extension..."
https://github.com/deforum-art/sd-webui-text2video.git extensions/sd-webui-text2video > /dev/null 2>&1

echo "Step 6: Installing opencv-python package..."
pip install opencv-python > /dev/null 2>&1

echo "Step 7: Installing python3-tk..."
sudo apt-get install -y python3-tk > /dev/null 2>&1

echo "Step 8: Installing mesa-utils..."
sudo apt-get install -y mesa-utils > /dev/null 2>&1

echo "Step 9: Installing libgl1-mesa-glx..."
sudo apt-get install -y libgl1-mesa-glx > /dev/null 2>&1

echo "Step 10: Running webui.sh script..."
bash webui.sh -f --share --xformers --enable-insecure-extension-access