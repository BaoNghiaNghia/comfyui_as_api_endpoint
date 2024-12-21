import os
from pathlib import Path
from celery import shared_task
from .services import check_current_queue

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))


@shared_task(name="backend.tasks.check_and_generate_images")
def check_and_generate_images():
    
    # Log the current folder path
    current_folder = check_current_queue()
    print(f"----- Current folder path: {current_folder}")
    
    min_files_threshold = 500  # Skip processing if file count exceeds this number

    # Ensure folder exists
    if not FILE_DIRECTORY.exists() or not FILE_DIRECTORY.is_dir():
        print(f"----- Folder '{FILE_DIRECTORY}' does not exist or is not a directory. Skipping.")
        return

    # Count files in the folder (excluding directories)
    file_count = sum(1 for file in FILE_DIRECTORY.iterdir() if file.is_file())

    if file_count < min_files_threshold:
        print(f"----- Folder has {file_count} files. Run generate image thumbnail AI.")
        generate_images_api()
    else:
        print(f"----- Folder has {file_count} files, skipping generation.")


def generate_images_api():
    # Simulated image generation logic
    print("Generating images...")
    # Add your custom image generation logic here
