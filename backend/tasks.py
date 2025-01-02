import os
import random
import asyncio
import datetime
from pathlib import Path
from celery import shared_task
from .services import check_current_queue, generate_images
from .constants import THUMBNAIL_STYLE_LIST, SUBFOLDER_TOOL_RENDER, SUBFOLDER_TEAM_AUTOMATION, MAX_IMAGES_THRESHOLD, COUNT_IMAGES_TO_DELETE, INIT_REQUEST

TEAM_AUTOMATION_FOLDER = Path(f"/thumbnail_img/{SUBFOLDER_TEAM_AUTOMATION}")
TOOL_RENDER_FOLDER = Path(f"/thumbnail_img/{SUBFOLDER_TOOL_RENDER}")


async def generate_images_api():
    """_summary_
        Asynchronous worker function to generate images based on API requests.
        This function processes a list of initial requests (INIT_REQUEST), determines the prefixes of file names,
        counts the occurrences of each prefix, and selects the prefix with the smallest count. It then randomly
        chooses a request with the selected prefix and calls the generate_images function with the details from
        the chosen request.
        Returns:
            None
    """

    prefixes = list({request["file_name"] for request in INIT_REQUEST})

    counts = {prefix: 0 for prefix in prefixes}
    for request in INIT_REQUEST:
        for prefix in prefixes:
            if request["file_name"].startswith(prefix):
                counts[prefix] += 1

    smallest_count = min(counts.values())
    smallest_prefixes = [prefix for prefix, count in counts.items() if count == smallest_count]

    today = datetime.datetime.now()
    day_of_week_number = today.weekday()  # Monday is 0, Sunday is 6
    print("Today is day number:", day_of_week_number)

    # Filter requests that match both the smallest prefixes and the current day of the week
    matching_objects = [
        request for request in INIT_REQUEST
        if request["file_name"] in smallest_prefixes and day_of_week_number in request["day_of_week"]
    ]

    # Ensure there's a valid request to process for today
    if not matching_objects:
        print("No matching objects for today's day of the week.")
        return

    random_request = random.choice(matching_objects)

    await generate_images(
        random_request["short_description"],        # short_description
        random_request["title"],                    # title
        1,                                          # thumbnail_number
        random.choice(THUMBNAIL_STYLE_LIST),        # thumb_style
        SUBFOLDER_TEAM_AUTOMATION,                  # subfolder
        random_request["file_name"]                 # filename_prefix
    )



@shared_task(name="backend.tasks.check_and_generate_images")
def check_and_generate_images():
    try:
        asyncio.run(generate_images_logic())

    except Exception as e:
        print(f"----- Error in worker `Generate images`: {e}")


async def generate_images_logic():
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
        if not os.path.isdir(TEAM_AUTOMATION_FOLDER):
            print(f"----- Folder '{TEAM_AUTOMATION_FOLDER}' does not exist or is not a directory. Skipping.")
            return

        # Count files in the directory
        file_count = sum(1 for file in os.listdir(TEAM_AUTOMATION_FOLDER) if os.path.isfile(os.path.join(TEAM_AUTOMATION_FOLDER, file)))

        # Check file count against the threshold
        if file_count < MAX_IMAGES_THRESHOLD:
            print(f"--------------------------------- START GENEREATING ------------------------------------")
            print(f"----- Folder has {file_count} files. Run generate image thumbnail AI Model until {MAX_IMAGES_THRESHOLD} files.")

            # Generate images asynchronously
            await generate_images_api()
        else:
            print(f"----- Folder has {file_count} files, skipping generation.")

    except Exception as e:
        print(f"----- Error generating images: {e}")


# Define the task to delete the oldest images
@shared_task(name="backend.tasks.delete_oldest_images_team_automation")
def delete_oldest_images_team_automation():
    try:
        # Get list of all image files in the folder sorted by modification time
        images = [
            os.path.join(TEAM_AUTOMATION_FOLDER, f) for f in os.listdir(TEAM_AUTOMATION_FOLDER)
            if os.path.isfile(os.path.join(TEAM_AUTOMATION_FOLDER, f))
        ]

        images.sort(key=os.path.getmtime)

        # Check if the number of images exceeds the threshold
        if len(images) > MAX_IMAGES_THRESHOLD:
            # Delete images until the number of images does not exceed the MAX_IMAGES_THRESHOLD
            while len(images) > MAX_IMAGES_THRESHOLD:
                # Delete the oldest 10 images if the total count exceeds MAX_IMAGES_THRESHOLD
                for i in range(min(COUNT_IMAGES_TO_DELETE, len(images))):
                    oldest_image = images[i]
                    os.remove(oldest_image)

                    print(f"--------------------------------- DELETE OLDEST IMAGES [TEAM AUTOMATION] ------------------------------------")
                    print(f"Deleted image: {oldest_image}")

                # Update the list of images after deletion
                images = [os.path.join(TEAM_AUTOMATION_FOLDER, f) for f in os.listdir(TEAM_AUTOMATION_FOLDER) if os.path.isfile(os.path.join(TEAM_AUTOMATION_FOLDER, f))]
                images.sort(key=os.path.getmtime)
        else:
            print(f"----- No need to delete images [Team Automation]. Current number of images ({len(images)}) is below the threshold ({MAX_IMAGES_THRESHOLD}).")

    except Exception as e:
        print(f"Error during image cleanup: {e}")


# Define the task to delete the oldest images
@shared_task(name="backend.tasks.delete_oldest_images_tool_render")
def delete_oldest_images_tool_render():
    try:
        # Get list of all image files in the folder sorted by modification time
        images = [
            os.path.join(TOOL_RENDER_FOLDER, f) for f in os.listdir(TOOL_RENDER_FOLDER)
            if os.path.isfile(os.path.join(TOOL_RENDER_FOLDER, f))
        ]

        images.sort(key=os.path.getmtime)

        if len(images) > MAX_IMAGES_THRESHOLD/2:
            while len(images) > MAX_IMAGES_THRESHOLD/2:
                for i in range(min(COUNT_IMAGES_TO_DELETE, len(images))):
                    oldest_image = images[i]
                    os.remove(oldest_image)

                    print(f"--------------------------------- DELETE OLDEST IMAGES [TOOL RENDER] ------------------------------------")
                    print(f"Deleted image: {oldest_image}")

                # Update the list of images after deletion
                images = [os.path.join(TOOL_RENDER_FOLDER, f) for f in os.listdir(TOOL_RENDER_FOLDER) if os.path.isfile(os.path.join(TOOL_RENDER_FOLDER, f))]
                images.sort(key=os.path.getmtime)
        else:
            print(f"----- No need to delete images [Tool Render]. Current number of images ({len(images)}) is below the threshold ({MAX_IMAGES_THRESHOLD/2}).")

    except Exception as e:
        print(f"Error during image cleanup: {e}")
