import os
import json
import logging
import requests
import asyncio
import random
import uuid
import websocket as ws_client
from dotenv import load_dotenv
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

server_address = os.getenv('COMFYUI_SERVER_ADDRESS', 'localhost:8188')
client_id = str(uuid.uuid4())


# Service to get image
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)
    with urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()


# Service to get history
def get_history(prompt_id):
    with urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())
    
    
# Service to queue a prompt
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urlopen(req).read())


# WebSocket image generation service
async def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
        else:
            continue

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output

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
        response.raise_for_status()  # Raise HTTPError for bad response codes

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

    # Randomly select a template and format it with the topic and textStyle
    selected_template = random.choice(scene_templates)
    formatted_template = selected_template.format(input_string=input_string, textStyle=textStyle)

    # Generate the final prompt
    prompt = f"```\n((Realistic photo)), ((perfect hand)), ((detailed)), ((best quality)), ((perfect tooth)), ((perfect eye))\n\n{formatted_template}```"

    return prompt


# Main image generation function
async def generate_images(positive_prompt, poster_number = 1):
    try:
        ws = ws_client.WebSocket()
        ws_url = f"ws://{server_address}/ws?clientId={client_id}"
        ws.connect(ws_url)

        with open("create-thumbnail-youtube-v3-api.json", "r", encoding="utf-8") as f:
            workflow_data = f.read()

        workflow = json.loads(workflow_data)
        noise_seed = random.randint(1, 1000000000000000)

        workflow["59"]["inputs"]["text1"] = (
            f'describe "{positive_prompt}" as a prompt base on this format prompt. '
            f'And must have banner title ***{positive_prompt}***:'
        )
        
        workflow["59"]["inputs"]["text2"] = create_prompt_and_call_api(positive_prompt)
        
        workflow["61"]["inputs"]["api_key"] = random.choice([
            "AIzaSyA1Z5slGG7kbIOWinCnuz4OJiJ3a6G0t7Y",
            "AIzaSyC1KVctwhDdVbIDv2cOZDa1kWyz0gq_jOQ",
            "AIzaSyA85MP5jctMT9rKVR6gT16tEmsuO4JqpLg",
            "AIzaSyCzXVTqFDI1a1XV5iLwIAcqY-bjR1Xpz8Y"
        ])
        
        workflow["29"]["inputs"]["batch_size"] = poster_number
        workflow["25"]["inputs"]["noise_seed"] = noise_seed

        # Fetch generated images
        images = await get_images(ws, workflow)
        ws.close()
        
        return images, noise_seed
    except Exception as e:
        # Handle exceptions and ensure WebSocket is closed if an error occurs
        if ws:
            ws.close()
        raise e
