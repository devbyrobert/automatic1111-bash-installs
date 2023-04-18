#!/bin/bash

echo "Step 1: Installing required packages..."
sudo apt install -y wget git python3 python3-venv > /dev/null 2>&1

echo "Step 2: Cloning stable-diffusion-webui repository..."
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git > /dev/null 2>&1

echo "Step 3: Changing directory to stable-diffusion-webui..."
cd stable-diffusion-webui

echo "Step 4: Downloading model to stable-diffusion-webui/models/Stable-diffusion..."
wget -q -O models/Realistic_Vision.ckpt https://huggingface.co/SG161222/Realistic_Vision_V2.0/resolve/main/Realistic_Vision_V2.0.ckpt

echo "Step 5: Installing sd-webui-controlnet extension..."
git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet > /dev/null 2>&1

echo "Step 6: Installing opencv-python package..."
pip install opencv-python > /dev/null 2>&1

echo "Step 7: Downloading control_sd15_depth.pth to stable-diffusion-webui/extensions/sd-webui-controlnet/models..."
wget -q -O extensions/sd-webui-controlnet/models/control_sd15_depth.pth https://huggingface.co/lllyasviel/ControlNet/resolve/main/models/control_sd15_depth.pth

echo "Step 8: Installing additional extensions..."
git clone https://github.com/Kahsolt/stable-diffusion-webui-prompt-travel.git extensions/stable-diffusion-webui-prompt-travel > /dev/null 2>&1
git clone https://github.com/deforum-art/deforum-for-automatic1111-webui.git extensions/deforum-for-automatic1111-webui > /dev/null 2>&1
git clone https://github.com/fkunn1326/openpose-editor.git extensions/openpose-editor > /dev/null 2>&1
git clone https://github.com/adieyal/sd-dynamic-prompts.git extensions/sd-dynamic-prompts > /dev/null 2>&1
git clone https://github.com/nonnonstop/sd-webui-3d-open-pose-editor.git extensions/sd-webui-3d-open-pose-editor > /dev/null 2>&1

echo "Step 9: Installing python3-tk..."
sudo apt-get install -y python3-tk > /dev/null 2>&1

echo "Step 10: Installing mesa-utils..."
sudo apt-get install -y mesa-utils > /dev/null 2>&1

echo "Step 11: Installing libgl1-mesa-glx..."
sudo apt-get install -y libgl1-mesa-glx > /dev/null 2>&1

echo "Step 12: Running webui.sh script..."
bash webui.sh -f --share --xformers --enable-insecure-extension-access