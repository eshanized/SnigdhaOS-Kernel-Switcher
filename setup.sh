#!/bin/bash
echo "Setting up Python environment..."
python -m venv "/home/whoami/Snigdha-OS-Kernel-Switcher/venv"
source "/home/whoami/Snigdha-OS-Kernel-Switcher/venv/bin/activate"
pip install --upgrade pip
pip install -r "/home/whoami/Snigdha-OS-Kernel-Switcher/requirements.txt"
deactivate
echo "Setup complete."
