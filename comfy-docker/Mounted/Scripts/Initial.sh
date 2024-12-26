#!/bin/bash

# change directory to ComfyUIDocker
cd /ComfyUIDocker

# Remove existing virtual environment in case a previous script run had failed or reinstalling
rm -rf /ComfyUIDocker/ComfyUIVirtualEnvironment

# Set up python virtual environment
python3 -m venv ComfyUIVirtualEnvironment

# Activate python virtual environment
source /ComfyUIDocker/ComfyUIVirtualEnvironment/bin/activate 

# If /ComfyUIDocker/ComfyUI already exists, move it to a backup folder of /ComfyUIDocker/ComfyUI_Backup_{DATE}
	sourceDir="/ComfyUIDocker/ComfyUI"
	# Check if the source directory exists
	if [ -d "$sourceDir" ]; then
	    # Define the backup directory with the current date/time
	    backupDir="/ComfyUIDocker/ComfyUI_Backup_$(date +%Y%m%d_%H%M%S)"

	    echo "Creating backup of previous ComfyUI install at $backupDir"   

	    # Move the source directory to the backup directory
	    mv "$sourceDir" "$backupDir"

	    echo "Backup created at $backupDir"   
	fi

# Clone ComfyUI from github
echo "====== Installing ComfyUI ======="
git clone https://github.com/comfyanonymous/ComfyUI

# install ComfyUI requirements
echo "====== Installing ComfyUI Requirements ======="
pip3 install -r /ComfyUIDocker/ComfyUI/requirements.txt

# install ComfyUI-Manager
echo "====== Installing ComfyUI Manager ======="
cd /ComfyUIDocker/ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager

echo "====== Installing ComfyUI Manager Requirements ======="
pip3 install -r /ComfyUIDocker/ComfyUI/custom_nodes/ComfyUI-Manager/requirements.txt

exit
