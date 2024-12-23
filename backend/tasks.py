import os
from pathlib import Path
from celery import shared_task
from .services import check_current_queue


FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))


@shared_task(name="backend.tasks.check_and_generate_images")
def check_and_generate_images():
    try:
        # Call the queue checking function
        queue_count = check_current_queue()

        # Handle the case where the queue_count is None
        if queue_count is None:
            print("----- Error: Could not fetch the current queue in AI Model. Skipping task execution.")
            return

        # Proceed if queue_count is valid
        if len(queue_count.get("queue_running", [])) > 0 or len(queue_count.get("queue_pending", [])) > 0:
            print(f"AI model is running another thumbnail images generation (Running: {len(queue_count.get('queue_running', []))}, Pending: {len(queue_count.get('queue_pending', []))}). Please try again later.")
            return


        min_files_threshold = 500

        # Check if the directory exists and is valid
        if not FILE_DIRECTORY.exists() or not FILE_DIRECTORY.is_dir():
            print(f"----- Folder '{FILE_DIRECTORY}' does not exist or is not a directory. Skipping.")
            return

        try:
            # Count files in the directory
            file_count = sum(1 for file in FILE_DIRECTORY.iterdir() if file.is_file())
        except Exception as e:
            print(f"----- Error counting files in folder '{FILE_DIRECTORY}': {e}")
            return

        # Check file count against the threshold
        if file_count < min_files_threshold:
            print(f"--------------------------------- START GENEREATING ------------------------------------")
            print(f"----- Folder has {file_count} files. Run generate image thumbnail AI.")

            try:
                generate_images_api()
            except Exception as e:
                print(f"----- Error generating images: {e}")
        else:
            print(f"----- Folder has {file_count} files, skipping generation.")

    except Exception as e:
        print(f"----- Error in worker `Generate images`: {e}")


def generate_images_api():
    print("Generating images...")
