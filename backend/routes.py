from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from transformers import AutoTokenizer, AutoModelForCausalLM

from .models import PromptRequest
from .services import generate_images, authenticate_user, download_single_image
from .tasks import check_and_generate_images
from .constants import DEFAULT_FILENAME_PREFIX, SUBFOLDER_TOOL_RENDER, FLUX_LORA_STEP


router = APIRouter()


@router.get("/")
async def get_index():
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    return FileResponse("ui/index.html")


# Endpoint to generate images
@router.get("/generate_llm")
async def prompt_llm():
    """
    Generate a response to a predefined prompt using a locally stored model.
    
    Args:
        max_length (int): The maximum length of the response.
        
    Returns:
        str: The generated response, or an error message if something goes wrong.
    """
    try:
        # "meta-llama/Meta-Llama-3.1-8B-Instruct"
        model_id = "D:\\Ytb Thumbnail AI\\Llama-3.2-1B"

        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

        messages = [
            # {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
            {"role": "user", "content": "Who are you?"},
        ]

        outputs = pipeline(
            messages,
            max_new_tokens=100,
        )
        
        return outputs[0]
    
    except Exception as e:
        # Handle exceptions and return a descriptive error message
        return f"An error occurred: {str(e)}"


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
