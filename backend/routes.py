from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from .models import PromptRequest
from .services import generate_images, authenticate_user, download_single_image
from .tasks import check_and_generate_images
from .constants import DEFAULT_FILENAME_PREFIX, SUBFOLDER_TOOL_RENDER


router = APIRouter()


@router.get("/")
async def get_index():
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """
    
    return FileResponse("ui/index.html")


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

        images = await generate_images(request.short_description, request.title, request.thumbnail_number, request.thumb_style, SUBFOLDER_TOOL_RENDER, DEFAULT_FILENAME_PREFIX)

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
