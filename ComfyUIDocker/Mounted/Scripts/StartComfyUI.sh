#!/bin/bash

# Activate python virtual environment
source /ComfyUIDocker/ComfyUIVirtualEnvironment/bin/activate 

# Start ComfyUI
python3 /ComfyUIDocker/ComfyUI/main.py --listen --port 8189 --extra-model-paths-config /ComfyUIDocker/extra_model_paths.yaml --temp-directory /tmp --output-directory /ComfyUIDocker/Outputs