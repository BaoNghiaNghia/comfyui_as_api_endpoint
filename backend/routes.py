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
        if request.thumbnail_number <= 0:
            raise HTTPException(status_code=400, detail="Thumbnail number must be greater than 0.")
        if not request.thumb_style:
            raise HTTPException(status_code=400, detail="Must be select style of thumbnail.")
        
        default_filename_prefix = 'ytbthumb'

        images = await generate_images(request.positive_prompt, request.thumbnail_number, request.thumb_style, "tool_render", default_filename_prefix)

        if not images:
            raise HTTPException(status_code=500, detail="Image generation failed.")

        return {"images": images, "thumbnail_number": request.thumbnail_number}

    except HTTPException as http_exc:
        raise http_exc

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=f"Value error: {str(value_error)}")

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"{str(exception)}")


@router.get("/download-images/")
async def download_file(file_name: str, subfolder: str):
    try:
        if not file_name or not subfolder:
            raise HTTPException(status_code=400, detail="Invalid file name or subfolder")
        
        file_path = FILE_DIRECTORY / subfolder / file_name
        if not file_path.resolve().is_relative_to(FILE_DIRECTORY.resolve()):
            raise HTTPException(status_code=400, detail="Invalid file path")

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            media_type="application/octet-stream",
            filename=file_name
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/check-and-generate/")
async def trigger_check_and_generate():
    task = check_and_generate_images.delay()  # Enqueue task
    return {"task_id": task.id, "status": "Task enqueued"}