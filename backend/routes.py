from fastapi import APIRouter, UploadFile, Form, HTTPException, Query
from typing import Annotated
import httpx
import json
import requests
import time
from datetime import datetime
from pathlib import Path
import asyncio

from fastapi.responses import FileResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
from ollama import chat
import base64
from ollama import ChatResponse

from .models import PromptRequest, LLMRequest, RewriteRequest
from .services import generate_images, authenticate_user, download_single_image
from .tasks import check_and_generate_images
from .constants import DEFAULT_FILENAME_PREFIX, SUBFOLDER_TOOL_RENDER, FLUX_LORA_STEP, SUBFOLDER_TEAM_AUTOMATION, INIT_50_ANIMAL_REQUEST

TEAM_AUTOMATION_FOLDER = Path(f"/thumbnail_img/{SUBFOLDER_TEAM_AUTOMATION}")

router = APIRouter()

@router.get("/")
async def get_index():
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    return FileResponse("ui/index.html")



@router.post("/rewrite_paragraph")
async def rewrite_paragraph(request: RewriteRequest):
    try:
        # Validate the input paragraph
        if not request.short_description:
            raise HTTPException(status_code=400, detail="Paragraph to rewrite is required.")
        
        # Prepare the payload for llama3.2
        payload = {
            "model": "llama3.2:3b",
            "messages": [
                {
                    "role": "user",
                    "content": f"Rewrite the following paragraph in a different style but keep the same meaning:\n\n{request.short_description}"
                }
            ]
        }

        # Send the request to the external API
        api_url = "http://host.docker.internal:11434/api/chat"
        response = requests.post(api_url, json=payload, stream=True)  # Use streaming response

        # Check response status
        if response.status_code == 200:
            response_text = ""
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        # Parse each chunk as a valid JSON object
                        chunk_data = json.loads(chunk.decode("utf-8"))
                        # Extract and append the content
                        response_text += chunk_data.get("message", {}).get("content", "")
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error: {e}")
                        continue  # Skip invalid chunks
            
            if response_text.strip():
                return {"original": request.short_description, "rewritten": response_text.strip()}
            else:
                raise HTTPException(status_code=500, detail="No valid response content received from Llama3.2.")

        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# Endpoint to generate images
@router.post("/generate_llm/image_caption")
async def generate_image_caption(request: LLMRequest):
    # Read the image content and encode it to base64
    try:
        if not request.short_description:
            raise HTTPException(status_code=400, detail="Short description is required.")
        if not request.file_path:
            raise HTTPException(status_code=400, detail="File name is required.")

        image_filename = Path(f"{request.file_path}")  # Image in the same directory
        # Read the image content and encode it to base64
        with open(image_filename, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
        
        # Send the POST request to the image captioning API
        response = requests.post("http://host.docker.internal:11434/api/chat", json={
            "model": 'llama3.2-vision',
            # "model": 'deepseek-r1',
            "messages": [
                {
                    "role": "user",
                    "content": request.short_description,
                    "images": [encoded_image]  # Use the base64-encoded image here
                }
            ]
        }, stream=True)  # Set stream=True to handle chunked responses
        
        # Check if the request was successful
        if response.status_code == 200:
            full_caption = ""
            # Iterate over each chunk of the response
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        chunk_data = chunk.decode('utf-8')
                        message = json.loads(chunk_data)
                        full_caption += message['message']['content']
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing chunk: {e}")
            
            # Print the final concatenated caption
            return full_caption.strip()
        else:
            print(f"Failed to get a valid response. Status Code: {response.status_code}")
            print("Response Text:", response.text)
            return {"error": "Request failed", "status_code": response.status_code, "response_text": response.text}

    except HTTPException as http_exception:
        raise http_exception

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=f"Value error: {str(value_error)}")

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"{str(exception)}")



# Endpoint to generate images
@router.get("/count_image")
async def count_image():
    try:
        today = datetime.now()
        day_of_week_number = today.weekday()  # Monday = 0, Sunday = 6

        # Filter requests that match today's day of the week
        valid_requests = [
            request for request in INIT_50_ANIMAL_REQUEST if day_of_week_number in request["day_of_week"]
        ]

        if not valid_requests:
            return {"message": "No valid requests for today's day of the week.", "counts": {}}

        # Extract prefixes from valid requests
        prefixes = list({request["file_name"] for request in valid_requests})

        # Initialize counts for each prefix
        counts = {prefix: 0 for prefix in prefixes}

        # Count files in the folder and subfolders matching each prefix
        if TEAM_AUTOMATION_FOLDER.exists() and TEAM_AUTOMATION_FOLDER.is_dir():
            for file in TEAM_AUTOMATION_FOLDER.rglob("*"):  # Recursively iterate through subfolders
                if file.is_file():
                    for prefix in prefixes:
                        if file.name.startswith(prefix):
                            counts[prefix] += 1
        else:
            raise HTTPException(status_code=404, detail=f"Folder not found: {TEAM_AUTOMATION_FOLDER}")

        # Sort the counts dictionary by value in descending order
        sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

        # Find the prefix with the smallest count
        smallest_count = min(counts.values())
        smallest_prefixes = [prefix for prefix, count in counts.items() if count == smallest_count]

        # Filter requests by the smallest prefixes
        matching_objects = [
            request for request in valid_requests if request["file_name"] in smallest_prefixes
        ]

        return {
            "total_count": len(sorted_counts),
            "counts": sorted_counts,
            "smallest_count": smallest_count,
            "smallest_prefixes": smallest_prefixes,
            # "matching_objects": matching_objects
        }

    except HTTPException as http_exception:
        raise http_exception

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=f"Value error: {str(value_error)}")

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"{str(exception)}")


# Endpoint to generate images
@router.post("/generate_images/thumbnail-youtube")
async def generate_images_api(request: PromptRequest):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    try:
        # # Authenticate if email and password are provided
        # if request.token:
        #     status_code, message = authenticate_user(request.domain, request.token)
        #     if status_code != 200:
        #         raise HTTPException(status_code=401, detail="Authentication failed")
        #     print(f"Authenticated successfully. Response: {message}")

        if not request.short_description:
            raise HTTPException(status_code=400, detail="Short description is required.")
        if not request.title:
            raise HTTPException(status_code=400, detail="Title is required.")
        if request.thumbnail_number <= 0:
            raise HTTPException(status_code=400, detail="Thumbnail number must be greater than 0.")
        if not request.thumb_style:
            raise HTTPException(status_code=400, detail="Must be select style of thumbnail.")

        images = await generate_images(request.short_description, request.title, request.thumbnail_number, request.thumb_style, SUBFOLDER_TOOL_RENDER, DEFAULT_FILENAME_PREFIX, FLUX_LORA_STEP['tool_render'])

        if not images:
            raise HTTPException(status_code=500, detail="Image generation failed.")

        return {"images": images, "thumbnail_number": request.thumbnail_number}

    except HTTPException as http_exception:
        raise http_exception

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=f"Value error: {str(value_error)}")

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"{str(exception)}")


@router.get("/download-images/")
async def download_file(file_name: str, subfolder: str):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    try:
        file_path = download_single_image(file_name, subfolder)

        return FileResponse(
            path=file_path,
            media_type="application/octet-stream",
            filename=file_name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/generate-prompt/")
async def generate_prompt():
    """_summary
        Function describe: Another solution for Gemini AI model, but limit token when using with alot of request. 
    """

    return 


@router.post("/check-and-generate/")
async def trigger_check_and_generate():
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    task = check_and_generate_images.delay()  # Enqueue task
    return {"task_id": task.id, "status": "Task enqueued"}
