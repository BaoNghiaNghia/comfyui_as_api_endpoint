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
        #         raise Exception("Authentication failed")

        #     print(f"Authenticated successfully. Response: {message}")

        images, seed = await generate_images(request.positive_prompt, request.poster_number)
        
        return images

        # # Convert images to a format FastAPI can return
        # image_responses = []
        # for node_id in images:
        #     for image_data in images[node_id]:
        #         img = Image.open(io.BytesIO(image_data))
        #         img_byte_arr = io.BytesIO()
        #         img.save(img_byte_arr, format='PNG')
        #         img_byte_arr.seek(0)

        #         # Append the image response to a list
        #         image_responses.append(StreamingResponse(img_byte_arr, media_type="image/png"))

        # return image_responses[0]  # Return the first image for simplicity
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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