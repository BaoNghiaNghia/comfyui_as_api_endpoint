import os
import json
import logging
import requests
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
ollama_server_address = os.getenv('OLLAMA_SERVER_ADDRESS', 'localhost:11434')
ollama_server_url = f"http://{ollama_server_address}/v1/chat/completions"
ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.1:latest')  # Load model from .env

system_prompt = """
    You are an AI model that transforms user input into concise, creative, and visually descriptive prompts for AI image generation. If the user input is empty, generate a creative, detailed description automatically. Always respond with a single, visually descriptive line, incorporating elements such as hyperrealistic, 4K, and detailed imagery when applicable.

    Guidelines:
    1. **Be Specific and Clear**: Ensure the response describes the subject, setting, and style in a visually engaging manner.
    2. **Keep It Brief**: Limit responses to one or two sentences that provide a vivid image while remaining concise.
    3. **Encourage Creativity**: Incorporate artistic styles like hyperrealism, 4K resolution, cinematic lighting, or surrealism where appropriate.
    4. **Handle Empty Input**: If the input is empty, create an imaginative and detailed prompt using the aforementioned elements.
    5. **No Extra Communication**: Respond only with the transformed prompt without additional commentary.

    ### Example Inputs and Outputs:

    **Input**: "A futuristic city at night with neon lights and flying cars."
    **Output**: "A neon-lit futuristic cityscape at night, with flying cars darting between towering skyscrapers, glowing in vibrant 4K detail."

    **Input**: "A serene beach with palm trees and a sunset."
    **Output**: "A serene beach at sunset, palm trees swaying gently as the golden light reflects off the 4K ocean waves."

    **Input**: "A magical forest with glowing trees and animals."
    **Output**: "A hyperrealistic forest where glowing trees light the way for mystical creatures under a twilight sky, captured in stunning 4K."

    **Input**: ""
    **Output**: "An intricately detailed 4K portrait of a warrior in golden armor, standing proudly under the dramatic glow of cinematic lighting."

    **Input**: "A watercolor painting of a rainy street."
    **Output**: "A dreamy watercolor painting of a rainy street, soft reflections glistening in the puddles under warm streetlights."
"""


# Service to get quick prompts data
def get_quick_prompts_data():
    with open("quick_prompts.json", "r") as f:
        return json.load(f)

# Service to ask LLM for response
def ask_llm_service(positive_prompt: str):
    ollama_request = {
        "model": ollama_model,  # Use model from .env
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": positive_prompt
            }
        ]
    }

    response = requests.post(ollama_server_url, json=ollama_request, headers={"Content-Type": "application/json"})
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

# Service to queue a prompt
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urlopen(req).read())

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
    topic = input_string.split('"')[1]
    
    # Generate the formatted prompt
    prompt = f"""((Realistic photo)), ((perfect hand)), ((detailed)), ((best quality)), ((perfect tooth)), ((perfect eye))
        Scene Description:
        A vibrant and festive Vietnamese Lunar New Year celebration. The scene features a bustling environment with traditional decorations: red lanterns hanging in the air, peach blossoms in full bloom, and kumquat trees adorned with golden fruits. In the foreground, people in colorful áo dài (traditional Vietnamese attire) are smiling and engaging in joyous activities such as giving red envelopes (lì xì) to children and enjoying Tết delicacies.

        Banner Title:
        The handwritten big text "{topic}" in top center

        Background Details:
        A lively village or urban setting decorated with banners handwritten big text "Happy New Year" in top center, strings of lights, and fireworks lighting up the evening sky. Market stalls and family gatherings add a sense of community and tradition.

        Color Palette:
        Dominated by auspicious colors like red and gold, symbolizing luck and prosperity, with hints of pink from peach blossoms and green from the kumquat trees. The lighting is warm and inviting, emphasizing the celebratory mood.

        Composition:
        The layout has a balanced mix of cultural symbols and joyful interactions. Focus on the details of traditional clothing, decorations, and facial expressions to capture the essence of Vietnamese New Year traditions."""
    
    # Prepare the data for the API request
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # API endpoint and headers
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Make the POST request
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print("API Response:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Main image generation function
async def generate_images(positive_prompt, poster_number):
    ws = ws_client.WebSocket()
    ws_url = f"ws://{server_address}/ws?clientId={client_id}"
    ws.connect(ws_url)

    with open("workflow.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    prompt_string = create_prompt_and_call_api(positive_prompt)

    workflow["6"]["inputs"]["text"] = prompt_string

    # Set a random seed for the KSampler node
    seed = random.randint(1, 1000000000000000)
    workflow["25"]["inputs"]["noise_seed"] = seed

    # Fetch generated images
    images = get_images(ws, workflow)
    ws.close()

    return images, seed
