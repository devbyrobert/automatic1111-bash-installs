#!/bin/bash

echo "Step 1: Installing required packages..."
sudo apt install -y wget git python3 python3-venv > /dev/null 2>&1
#!/bin/bash

echo "Step 1: Installing required packages..."
sudo apt install -y wget git python3 python3-venv > /dev/null 2>&1

echo "Step 2: Cloning stable-diffusion-webui repository..."
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git > /dev/null 2>&1

echo "Step 3: Changing directory to stable-diffusion-webui..."
cd stable-diffusion-webui

echo "Step 4: Downloading model to stable-diffusion-webui/models/Stable-diffusion..."
wget -q -O models/Inkpunk-Diffusion-v2.ckpt https://huggingface.co/Envvi/Inkpunk-Diffusion/resolve/main/Inkpunk-Diffusion-v2.ckpt

echo "Step 5: Installing sd-webui-controlnet extension..."
git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet > /dev/null 2>&1

echo "Step 6: Installing opencv-python package..."
pip install opencv-python > /dev/null 2>&1

echo "Step 7: Downloading ControlNet models to stable-diffusion-webui/extensions/sd-webui-controlnet/models..."
wget -q -O extensions/sd-webui-controlnet/models/control_sd15_openpose.pth https://huggingface.co/lllyasviel/ControlNet/resolve/main/models/control_sd15_openpose.pth

echo "Step 8: Installing python3-tk..."
sudo apt-get install -y python3-tk > /dev/null 2>&1

echo "Step 9: Installing mesa-utils..."
sudo apt-get install -y mesa-utils > /dev/null 2>&1

echo "Step 10: Installing libgl1-mesa-glx..."
sudo apt-get install -y libgl1-mesa-glx > /dev/null 2>&1

echo "Step 11: Running webui.sh script..."
bash webui.sh -f --share --xformers --enable-insecure-extension-access