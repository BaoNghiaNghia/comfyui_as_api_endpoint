import os
import json
from pathlib import Path
from celery import shared_task
from .services import check_current_queue, generate_images


FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))
MAX_IMAGES_THRESHOLD = 500
IMAGES_TO_DELETE = 5


async def generate_images_api():
    init_request = {
        "positive_prompt": "Happy New Year",
        "thumbnail_number": 5,
        "thumb_style": "realistic photo",
    }

    await generate_images(init_request["positive_prompt"], init_request["thumbnail_number"], init_request["thumb_style"])

    # Convert the response into a JSON serializable format if needed
    # return json.dumps(images)  # Assuming `images` is a JSON-serializable object


@shared_task(name="backend.tasks.check_and_generate_images")
async def check_and_generate_images():
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
        if file_count < MAX_IMAGES_THRESHOLD:
            print(f"--------------------------------- START GENEREATING ------------------------------------")
            print(f"----- Folder has {file_count} files. Run generate image thumbnail AI Model until {MAX_IMAGES_THRESHOLD} files.")

            # try:
            #     await generate_images_api()
            # except Exception as e:
            #     print(f"----- Error generating images: {e}")
        else:
            print(f"----- Folder has {file_count} files, skipping generation.")

    except Exception as e:
        print(f"----- Error in worker `Generate images`: {e}")
        
# Define the task to delete the oldest images
@shared_task(name="backend.tasks.delete_oldest_images")
def delete_oldest_images():
    try:
        # Get list of all image files in the folder sorted by modification time
        images = [
            os.path.join(FILE_DIRECTORY, f) for f in os.listdir(FILE_DIRECTORY)
            if os.path.isfile(os.path.join(FILE_DIRECTORY, f))
        ]
        images.sort(key=os.path.getmtime)

        # Delete images until the number of images does not exceed the MAX_IMAGES_THRESHOLD
        while len(images) > MAX_IMAGES_THRESHOLD:
            # Delete the oldest 10 images if the total count exceeds MAX_IMAGES_THRESHOLD
            for i in range(min(IMAGES_TO_DELETE, len(images))):
                oldest_image = images[i]  # Get the i-th oldest image
                os.remove(oldest_image)

                print(f"--------------------------------- DELETE OLDEST IMAGES ------------------------------------")
                print(f"Deleted image: {oldest_image}")
            
            # Update the list of images after deletion
            images = [
                os.path.join(FILE_DIRECTORY, f) for f in os.listdir(FILE_DIRECTORY)
                if os.path.isfile(os.path.join(FILE_DIRECTORY, f))
            ]
            images.sort(key=os.path.getmtime)

    except Exception as e:
        print(f"Error during image cleanup: {e}")
