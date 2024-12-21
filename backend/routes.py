from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from .models import PromptRequest
from .services import generate_images, authenticate_user
from PIL import Image
import io
from pathlib import Path
from .tasks import check_and_generate_images

router = APIRouter()

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))


@router.get("/")
async def get_index():
    return FileResponse("ui/index.html")


# Endpoint to generate images
@router.post("/generate_images/thumbnail-youtube")
async def generate_images_api(request: PromptRequest):
    try:
        # # Authenticate if email and password are provided
        # if request.token:
        #     status_code, message = authenticate_user(request.domain, request.token)
        #     if status_code != 200:
        #         raise HTTPException(status_code=401, detail="Authentication failed")

        #     print(f"Authenticated successfully. Response: {message}")

        # Validate request fields
        if not request.positive_prompt:
            raise HTTPException(status_code=400, detail="Positive prompt is required.")
        if request.poster_number <= 0:
            raise HTTPException(status_code=400, detail="Poster number must be greater than 0.")
        if not request.thumb_style:
            raise HTTPException(status_code=400, detail="Must be select style of thumbnail.")

        # Generate images
        images, seed = await generate_images(request.positive_prompt, request.poster_number, request.thumb_style)

        # Check if images are generated successfully
        if not images:
            raise HTTPException(status_code=500, detail="Image generation failed.")

        return {"images": images, "seed": seed}

    except HTTPException as http_exc:
        # Re-raise known HTTP exceptions
        raise http_exc

    except ValueError as value_error:
        # Handle specific errors (e.g., invalid input)
        raise HTTPException(status_code=400, detail=f"Value error: {str(value_error)}")

    except Exception as exception:
        # Handle unexpected exceptions
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exception)}")


@router.get("/download-images/")
async def download_file(file_name: str):
    file_path = FILE_DIRECTORY / file_name
    if not file_path.exists() or not file_path.is_file():
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",  # Generic binary file type
        filename=file_name  # The name for the downloaded file
    )

@router.post("/check-and-generate/")
async def trigger_check_and_generate():
    task = check_and_generate_images.delay()  # Enqueue task
    return {"task_id": task.id, "status": "Task enqueued"}