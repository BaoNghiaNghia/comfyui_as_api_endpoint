import os
import json
import logging
import requests
import random
import uuid
import websocket
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


COMFY_UI_SERVER_ADDRESS = os.getenv('host.docker.internal:8188', 'host.docker.internal:8188')
CLIENT_ID = str(uuid.uuid4())
BACKEND_SERVER_ADDRESS = os.getenv('BACKEND_SERVER_ADDRESS', 'host.docker.internal:8000')

REMOTE_SERVER_ADDRESS = os.getenv('REMOTE_SERVER_ADDRESS', 'host.docker.internal:8188')

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)

    with urlopen(f"http://{COMFY_UI_SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()


# Service to get history
def get_history(prompt_id):
    with urlopen(f"http://{COMFY_UI_SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())


# Service to queue a prompt
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


def create_prompt_and_call_api(input_string):
    # Randomly choose a text style
    textStyle = random.choice(["The handwritten big text", "The title of the movie is"])

    # Scene templates
    scene_templates = [
        """
            Scene Description:

            A vibrant and festive Vietnamese Lunar New Year celebration. The scene features a bustling environment with traditional decorations: red lanterns hanging in the air, peach blossoms in full bloom, and kumquat trees adorned with golden fruits. In the foreground, people in colorful áo dài (traditional Vietnamese attire) are smiling and engaging in joyous activities such as giving red envelopes (lì xì) to children and enjoying Tết delicacies.


            Banner Title:

            {textStyle} "{input_string}" in top center


            Background Details:

            A lively village or urban setting decorated with banners handwritten big text "Happy New Year" in top center, strings of lights, and fireworks lighting up the evening sky. Market stalls and family gatherings add a sense of community and tradition.

            Color Palette:

            Dominated by auspicious colors like red and gold, symbolizing luck and prosperity, with hints of pink from peach blossoms and green from the kumquat trees. The lighting is warm and inviting, emphasizing the celebratory mood.


            Composition:

            The layout has a balanced mix of cultural symbols and joyful interactions. Focus on the details of traditional clothing, decorations, and facial expressions to capture the essence of Vietnamese New Year traditions.
        """,
        """
            Overall Theme:

            Relaxed, nostalgic, and cozy.


            Main Colors:

            Soft pastels: Dusty pink, muted teal, beige, and brown tones.
            Contrasting accents: Soft yellow or lavender.


            Style: 

            Nostalgic, cozy, slightly melancholic.


            Character Illustration:

            A person (animated or realistic) sitting by a desk or bed with headphones on, studying or doodling.
            Clothing: Oversized sweater, cozy attire.
            Environment: Rainy window with streaks of water, a desk lamp casting warm light.


            Background:

            A small, cluttered room filled with books, plants, and a glowing laptop.
            Outside the window: Rain, autumn leaves, or a nighttime city view.


            Lighting Effects:

            Dim ambient lighting with a warm glow from a desk lamp or fairy lights.


            Font Style:

            Handwritten, script-like fonts for a nostalgic vibe (e.g., "Pacifico").


            Text Ideas:

            {textStyle} “{input_string}”


            Decorative Elements:

            Vinyl records spinning on a turntable.
            Animated-style clouds or stars floating subtly in the background.
        """
    ]

    selected_template = random.choice(scene_templates)
    formatted_template = selected_template.format(input_string=input_string, textStyle=textStyle)

    return f"```\n((Realistic photo)), ((perfect hand)), ((detailed)), ((best quality)), ((perfect tooth)), ((perfect eye))\n\n{formatted_template}```"


async def generate_images(positive_prompt, thumbnail_number=1, thumb_style='realistic photo', subfolder='tool_render', filename_prefix='ytbthumb'):
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
            f'describe "{positive_prompt}" with {thumb_style} style as a prompt base on this format prompt.'
            f'And must have banner title ***{positive_prompt}***:'
        )

        workflow["59"]["inputs"]["text2"] = create_prompt_and_call_api(positive_prompt)

        workflow["61"]["inputs"]["api_key"] = random.choice([
            "AIzaSyA1Z5slGG7kbIOWinCnuz4OJiJ3a6G0t7Y",
            "AIzaSyC1KVctwhDdVbIDv2cOZDa1kWyz0gq_jOQ",
            "AIzaSyA85MP5jctMT9rKVR6gT16tEmsuO4JqpLg",
            "AIzaSyCzXVTqFDI1a1XV5iLwIAcqY-bjR1Xpz8Y"
        ])
        

        workflow["29"]["inputs"]["batch_size"] = thumbnail_number
        workflow["25"]["inputs"]["noise_seed"] = noise_seed

        # Fetch generated images
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
