import os
import json
import logging
import requests
import random
import websocket
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from fastapi import HTTPException
from urllib.parse import urlencode
from .constants import GEMINI_KEY_TOOL_RENDER, GEMINI_KEY_TEAM_AUTOMATION, SUBFOLDER_TEAM_AUTOMATION, SUBFOLDER_TOOL_RENDER, CLIENT_ID


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


COMFY_UI_SERVER_ADDRESS = os.getenv('host.docker.internal:8188', 'host.docker.internal:8188')
BACKEND_SERVER_ADDRESS = os.getenv('BACKEND_SERVER_ADDRESS', 'host.docker.internal:8000')

REMOTE_SERVER_ADDRESS = os.getenv('REMOTE_SERVER_ADDRESS', 'host.docker.internal:8188')

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)

    with urlopen(f"http://{COMFY_UI_SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()


def get_history(prompt_id):
    with urlopen(f"http://{COMFY_UI_SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = Request(f"http://{COMFY_UI_SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urlopen(req).read())


def check_current_queue():
    try:
        req = Request(f"http://{COMFY_UI_SERVER_ADDRESS}/queue")

        with urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data)

    except HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")

    except URLError as e:
        print(f"URLError: {e.reason}")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    return None


async def get_images(ws, prompt, noise_seed):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    last_reported_percentage = 0

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'progress':
                data = message['data']
                current_progress = data['value']
                max_progress = data['max']
                percentage = int((current_progress / max_progress) * 100)

                if percentage >= last_reported_percentage + 10:
                    last_reported_percentage = percentage
                    logging.info(f"PromptID: {prompt_id} - Process: {percentage} %")

            elif message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break

        else:
            continue

    history = get_history(prompt_id)[prompt_id]

    output_images = history['outputs']["178"]['images']
    for output_image in output_images:
        output_image['file_path'] = f"http://{REMOTE_SERVER_ADDRESS}/download-images?file_name={output_image['filename']}&subfolder={output_image['subfolder']}"
        output_image['seed'] = noise_seed

    return output_images


def authenticate_user(domain, token):
    try:
        if not domain or not token:
            raise ValueError("Domain, token must be provided for authentication")

        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer ' + token
        }

        response = requests.get(domain, headers=headers)
        response.raise_for_status()

        logging.info(f"Authentication successful with domain {domain}")
        return response.status_code, response.reason

    except ValueError as ve:
        logging.error(f"Authentication failed: {ve}")
        return None

    except requests.exceptions.RequestException as re:
        logging.error(f"Request error during authentication: {re}")
        return None

    except Exception as e:
        logging.error(f"An unexpected error occurred during authentication: {e}")
        return None


def scene_template_1(textStyle, input_string, title):
    return f"""
        Scene Description:

        A vibrant and festive Vietnamese Lunar New Year celebration. The scene features a bustling environment with traditional decorations: red lanterns hanging in the air, peach blossoms in full bloom, and kumquat trees adorned with golden fruits. In the foreground, people in colorful áo dài (traditional Vietnamese attire) are smiling and engaging in joyous activities such as giving red envelopes to children and enjoying Tết delicacies.


        Banner Title:

        {textStyle} "{title}" in top center


        Background Details:

        A lively village or urban setting decorated with banners handwritten big text "Happy New Year" in top center, strings of lights, and fireworks lighting up the evening sky. Market stalls and family gatherings add a sense of community and tradition.


        Color Palette:

        Dominated by auspicious colors like red and gold, symbolizing luck and prosperity, with hints of pink from peach blossoms and green from the kumquat trees. The lighting is warm and inviting, emphasizing the celebratory mood.


        Composition:

        The layout has a balanced mix of cultural symbols and joyful interactions. Focus on the details of traditional clothing, decorations, and facial expressions to capture the essence of Vietnamese New Year traditions.
    """


def scene_template_2(textStyle, input_string, title):
    return f"""
        ...
    """


def scene_template_3(textStyle, input_string, title):
    return f"""
        ...
    """


def scene_template_4(textStyle, input_string, title):
    return f"""
        ...
    """


def create_prompt_and_call_api(input_string, title):
    # Mapping of scene templates
    scene_templates = {
        1: scene_template_1,
        2: scene_template_1,
        3: scene_template_1,
        4: scene_template_1
    }

    # Randomly choose a text style
    textStyle = random.choice(["The handwritten big text", "The title of the movie is"])

    # Randomly choose a scene template
    template_choice = random.choice([1, 2, 3, 4])
    scene_template = scene_templates[template_choice](textStyle, input_string, title)

    # Construct and return the full API call prompt
    return f"```\n((Realistic photo)), ((perfect hand)), ((detailed)), ((best quality)), ((perfect tooth)), ((perfect eye))\n\n{scene_template}```"



async def generate_images(short_description, title, thumbnail_number=1, thumb_style='realistic photo', subfolder='tool_render', filename_prefix='ytbthumb'):
    ws = None

    try:
        ws = websocket.WebSocket()
        ws_url = f"ws://{COMFY_UI_SERVER_ADDRESS}/ws?clientId={CLIENT_ID}"

        try:
            ws.connect(ws_url)
        except websocket.WebSocketConnectionClosedException as e:
            raise ConnectionError(f"Could not establish WebSocket connection: {e}")
        except Exception as e:
            raise Exception(f"Model AI Stopped: {e}")

        # Check if AI model is running queue
        queue_count = check_current_queue()

        if len(queue_count["queue_running"]) > 0 or len(queue_count["queue_pending"]) > 0:
            raise Exception(f'AI model is running another thumbnail images generation (Running: {len(queue_count["queue_running"])}, Pending: {len(queue_count["queue_pending"])}). Please try again later.')

        with open("create-thumbnail-youtube-v3-api.json", "r", encoding="utf-8") as f:
            workflow_data = f.read()

        workflow = json.loads(workflow_data)
        noise_seed = random.randint(1, 1000000000000000)

        workflow["178"]["inputs"]["foldername_prefix"] = subfolder
        workflow["178"]["inputs"]["filename_prefix"] = filename_prefix

        workflow["59"]["inputs"]["text1"] = (
            f'describe "{short_description}" with {thumb_style} style as a prompt base on this format prompt.'
            f'And must have banner title ***{title}***:'
        )

        workflow["59"]["inputs"]["text2"] = create_prompt_and_call_api(short_description, title)

        if subfolder == SUBFOLDER_TOOL_RENDER:
            api_key_list = GEMINI_KEY_TOOL_RENDER
        elif subfolder == SUBFOLDER_TEAM_AUTOMATION:
            api_key_list = GEMINI_KEY_TEAM_AUTOMATION
        else:
            raise ValueError(f"Unsupported subfolder: {subfolder}")

        workflow["61"]["inputs"]["api_key"] = random.choice(api_key_list)

        workflow["29"]["inputs"]["batch_size"] = thumbnail_number
        workflow["25"]["inputs"]["noise_seed"] = noise_seed

        images = await get_images(ws, workflow, noise_seed)
        return images

    except ConnectionError as ce:
        raise ce
    except FileNotFoundError as fnfe:
        raise fnfe
    except Exception as e:
        raise e

    finally:
        if ws:
            try:
                ws.close()
            except Exception as e:
                raise "Network error"


def download_single_image(file_name: str, subfolder: str):
    try:
        if not file_name or not subfolder:
            raise HTTPException(status_code=400, detail="Invalid file name or subfolder")
        
        file_path = FILE_DIRECTORY / subfolder / file_name
        
        if not file_path.resolve().is_relative_to(FILE_DIRECTORY.resolve()):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        return file_path

    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the file")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File or directory not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
