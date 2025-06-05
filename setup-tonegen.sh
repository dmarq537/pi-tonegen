#!/bin/bash

echo "Updating system..."
sudo apt update && sudo apt install -y python3 python3-pip python3-tk portaudio19-dev

echo "Installing Python packages..."
pip3 install numpy pyaudio

echo "Downloading tone generator script..."
curl -sSL https://raw.githubusercontent.com/dmarq537/pi-tonegen/main/tonegen_pi1.py -o ~/tonegen_pi1.py
chmod +x ~/tonegen_pi1.py

echo "Done! Run the tone generator with: python3 ~/tonegen_pi1.py"
