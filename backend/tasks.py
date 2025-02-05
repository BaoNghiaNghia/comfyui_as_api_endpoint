import os
import random
import asyncio
from datetime import datetime
import json
import numpy as np
from pathlib import Path
from celery import shared_task
from .services import check_current_queue, generate_images
from .constants import THUMBNAIL_STYLE_LIST, SUBFOLDER_TOOL_RENDER, SUBFOLDER_TEAM_AUTOMATION, MAX_IMAGES_THRESHOLD, COUNT_IMAGES_TO_DELETE, INIT_50_ANIMAL_REQUEST, THUMBNAIL_PER_TIMES, FLUX_LORA_STEP

TEAM_AUTOMATION_FOLDER = Path(f"/thumbnail_img/{SUBFOLDER_TEAM_AUTOMATION}")


TOOL_RENDER_FOLDER = Path(f"/thumbnail_img/{SUBFOLDER_TOOL_RENDER}")

async def render_random_from_init_request():
    """
    Render a random image from the INIT_50_ANIMAL_REQUEST list when there are no files in the folder.
    Only selects requests matching the current day of the week.
    """
    if not INIT_50_ANIMAL_REQUEST:
        print("----- No requests in INIT_50_ANIMAL_REQUEST. Cannot render a random image.")
        return

    today = datetime.now()
    day_of_week_number = today.weekday()  # Monday is 0, Sunday is 6

    # Filter requests matching the current day of the week
    valid_requests = [
        request for request in INIT_50_ANIMAL_REQUEST if day_of_week_number in request["day_of_week"]
    ]

    if not valid_requests:
        print("----- No valid requests in INIT_50_ANIMAL_REQUEST for today's day of the week.")
        return

    # Select a random request
    random_request = random.choice(valid_requests)
    file_name = random_request["file_name"]

    # Define the correct subfolder path
    folder_path = TEAM_AUTOMATION_FOLDER / file_name
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure folder exists

    print(f"----- Rendering a random image for request: {file_name} in {folder_path}")

    # # Ensure short_description is not empty
    if not random_request["short_description"]:
        print(f"Warning: No descriptions found for {file_name}. Skipping image generation.")
        return

    selected_description = random.choice(random_request["short_description"])

    await generate_images(
        selected_description,                                                               # short_description
        random_request["title"] or "Untitled",                                              # title (fallback to "Untitled" if empty)
        THUMBNAIL_PER_TIMES,                                                                # thumbnail_number
        random.choice(THUMBNAIL_STYLE_LIST),                                                # thumb_style
        str(Path(f"/{SUBFOLDER_TEAM_AUTOMATION}") / file_name),                             # ✅ Save inside the correct subfolder
        file_name,                                                                          # filename_prefix
        FLUX_LORA_STEP['team_automation']                                                   # step
    )


async def generate_images_api():
    """
    Asynchronous worker function to generate images based on API requests.
    """
    today = datetime.now()
    day_of_week_number = today.weekday()  # Monday = 0, Sunday = 6

    # Filter requests that match today's day of the week
    valid_requests = [
        request for request in INIT_50_ANIMAL_REQUEST if day_of_week_number in request["day_of_week"]
    ]

    if not valid_requests:
        print("No valid requests for today's day of the week.")
        return {"message": "No valid requests for today.", "counts": {}}

    # Extract prefixes from valid requests
    prefixes = list({request["file_name"] for request in valid_requests})

    # Initialize counts for each prefix
    counts = {prefix: 0 for prefix in prefixes}

    # Count files in the folder and subfolders matching each prefix
    if TEAM_AUTOMATION_FOLDER.exists() and TEAM_AUTOMATION_FOLDER.is_dir():
        for file in TEAM_AUTOMATION_FOLDER.rglob("*"):  # Recursively iterate through subfolders
            if file.is_file():
                for prefix in prefixes:
                    if file.stem.startswith(prefix):  # Check filename without extension
                        counts[prefix] += 1

    if not counts:
        return {"message": "No existing files found for comparison.", "counts": {}}

    # Find the prefix with the smallest count
    smallest_count = min(counts.values())
    smallest_prefixes = [prefix for prefix, count in counts.items() if count == smallest_count]
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    # If smallest_prefixes is empty, get a random prefix from counts
    if not smallest_prefixes:
        smallest_prefixes = [random.choice(list(counts.keys()))]

    print(f"-------------------------------------------------")
    print(json.dumps(sorted_counts, indent=4))
    print(f"-------------------------------------------------")

    # Filter requests by the smallest prefixes
    matching_objects = [
        request for request in valid_requests if request["file_name"] in smallest_prefixes
    ]

    if not matching_objects:
        print("No matching objects after filtering by prefixes.")
        return {"message": "No matching objects found.", "counts": counts}

    # Select a random request from the matching objects
    random_request = random.choice(matching_objects)

    # Ensure short_description is not empty
    if not random_request["short_description"]:
        print(f"Warning: No descriptions found for {random_request['file_name']}.")
        return {"message": f"No descriptions available for {random_request['file_name']}"}

    selected_description = random.choice(random_request["short_description"])

    print(f"Processing request: {random_request['file_name']}")
    print(f"Selected Description: {selected_description}")

    # ✅ FIX: Convert write_path to string to avoid JSON serialization error
    write_path = Path(f"/{SUBFOLDER_TEAM_AUTOMATION}") / random_request["file_name"]
    await generate_images(
        selected_description,                                                       # short_description
        random_request["title"],                                                    # title (fallback to "Untitled" if empty)
        THUMBNAIL_PER_TIMES,                                                        # thumbnail_number
        random.choice(THUMBNAIL_STYLE_LIST),                                        # thumb_style
        str(write_path),                                                            # ✅ Convert Path object to string
        random_request["file_name"],                                                # filename_prefix
        FLUX_LORA_STEP['team_automation']
    )




@shared_task(name="backend.tasks.check_and_generate_images")
def check_and_generate_images():
    try:
        asyncio.run(generate_images_logic())

    except Exception as e:
        print(f"----- Error in worker `Generate images`: {e}")


async def generate_images_logic():
    """
    Function describe: This function is used to generate images based on the current queue status and the number of images in the folder.
    """
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
        if not TEAM_AUTOMATION_FOLDER.is_dir():
            print(f"----- Folder '{TEAM_AUTOMATION_FOLDER}' does not exist or is not a directory. Skipping.")
            return

        # Count files in all subfolders
        file_count = sum(1 for subfolder in TEAM_AUTOMATION_FOLDER.iterdir() if subfolder.is_dir() 
                         for file in subfolder.iterdir() if file.is_file())

        # Count all folders (directories) inside TEAM_AUTOMATION_FOLDER
        folder_count = sum(1 for item in TEAM_AUTOMATION_FOLDER.iterdir() if item.is_dir())

        print(f"----- {file_count} files and {folder_count} subfolders.")

        # Check file count against the threshold
        if folder_count == 0:
            print("----- Folder has no files. Rendering a random image from INIT_50_ANIMAL_REQUEST.")
            await render_random_from_init_request()
            return

        if file_count < MAX_IMAGES_THRESHOLD:
            print(f"--------------------------------- START GENERATING ------------------------------------")
            print(f"----- Folder has {file_count} files and {folder_count} folders. Running image generation until {MAX_IMAGES_THRESHOLD} files.")

            # Generate images asynchronously
            await generate_images_api()
        else:
            print(f"----- Folder has {file_count} files, skipping generation.")

    except Exception as e:
        print(f"----- Error generating images: {e}")

 

# Define the task to delete the oldest images
@shared_task(name="backend.tasks.delete_oldest_images_team_automation")
def delete_oldest_images_team_automation():
    """_summary
        Function describe: This function is used to delete the oldest images in the Team Automation folder.
    """
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
    """_summary
        Function describe: This function is used to delete the oldest images in the Tool Render folder.
    """

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
