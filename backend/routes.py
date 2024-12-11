from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from .models import LLMRequest, PromptRequest
from .services import generate_images, get_quick_prompts_data, ask_llm_service, authenticate_user
from PIL import Image
import io
from pathlib import Path

router = APIRouter()

@router.get("/")
async def get_index():
    return FileResponse("ui/index.html")

# Endpoint to serve quick prompts from configuration file
@router.get("/quick_prompts/")
async def get_quick_prompts():
    try:
        prompts = get_quick_prompts_data()
        return JSONResponse(content=prompts)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading quick prompts file.")

# Endpoint to ask the LLM for creative ideas based on the positive prompt
@router.post("/ask_llm/")
async def ask_llm(request: LLMRequest):
    try:
        response = ask_llm_service(request.positive_prompt)
        return JSONResponse(content={"assistant_reply": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with LLM: " + str(e))

# Endpoint to generate images
@router.post("/generate_images/thumbnail-youtube")
async def generate_images_api(request: PromptRequest):
    try:
        # Authenticate if email and password are provided
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

        # Generate images
        images, seed = await generate_images(request.positive_prompt, request.poster_number)

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


# Specify the directory where files are stored
FILE_DIRECTORY = Path("files")  # Update this to your directory path

@router.post("/download-images/")
async def download_file(file_name: str):
    file_path = FILE_DIRECTORY / file_name
    if not file_path.exists() or not file_path.is_file():
        return {"error": "File not found"}
    
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",  # Generic binary file type
        filename=file_name  # The name for the downloaded file
    )