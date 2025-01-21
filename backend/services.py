import os
import json
import logging
import random
import asyncio
import requests
import websocket
from urllib.parse import urlencode
from fastapi import HTTPException
from .constants import CLIENT_ID, FILE_DIRECTORY, FLUX_LORA_STEP, SUBFOLDER_TOOL_RENDER, SUBFOLDER_TEAM_AUTOMATION, GEMINI_KEY_TOOL_RENDER, GEMINI_KEY_TEAM_AUTOMATION, THUMBNAIL_SIZES



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

COMFY_UI_SERVER_ADDRESS = os.getenv('COMFY_UI_SERVER_ADDRESS', 'host.docker.internal:8188')
BACKEND_SERVER_ADDRESS = os.getenv('BACKEND_SERVER_ADDRESS', 'host.docker.internal:8000')
# REMOTE_SERVER_ADDRESS = os.getenv('REMOTE_SERVER_ADDRESS', 'host.docker.internal:8000')
REMOTE_SERVER_ADDRESS = os.getenv('REMOTE_SERVER_ADDRESS', 'sscauto.ddns.net:8000')

# Choose a text style (consider making this configurable or less random)
TEXT_STYLE = "A clean and modern sans-serif" # Consider: random.choice(["The handwritten big text", "A clean and modern sans-serif "])

# Use a session for connection pooling
session = requests.Session()



def get_image(filename, subfolder, folder_type):
    """Retrieves an image from the ComfyUI server."""
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urlencode(data)
    url = f"http://{COMFY_UI_SERVER_ADDRESS}/view?{url_values}"

    try:
        with session.get(url, stream=True) as response:
            response.raise_for_status()
            return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching image: {e}")
        raise


def get_history(prompt_id):
    """Retrieves the history for a given prompt ID from the ComfyUI server."""
    url = f"http://{COMFY_UI_SERVER_ADDRESS}/history/{prompt_id}"
    try:
        with session.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching history: {e}")
        raise


def queue_prompt(prompt):
    """Queues a prompt on the ComfyUI server."""
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    url = f"http://{COMFY_UI_SERVER_ADDRESS}/prompt"

    try:
        with session.post(url, data=data) as response:
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error queuing prompt: {e}")
        raise


def check_current_queue():
    """Checks the current queue on the ComfyUI server."""
    url = f"http://{COMFY_UI_SERVER_ADDRESS}/queue"

    try:
        with session.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking queue: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error checking queue: {str(e)}")
        return None


async def get_images(ws, prompt, noise_seed):
    """Retrieves images generated from a prompt, handling WebSocket communication."""
    prompt_id = queue_prompt(prompt)['prompt_id']
    last_reported_percentage = 0

    try:
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

        # Fetch history and validate structure
        history = get_history(prompt_id).get(prompt_id, {})
        output_data = history.get('outputs', {}).get("178", {}) # Access 'outputs' safely
        images = output_data.get('images', [])

        # Process images
        for output_image in images:
            try:
                filename = output_image['filename']
                subfolder = output_image['subfolder']
                output_image['file_path'] = f"http://{REMOTE_SERVER_ADDRESS}/download-images?file_name={filename}&subfolder={subfolder}"
                output_image['seed'] = noise_seed
            except KeyError as e:
                logging.warning(f"Missing key in image data: {e}")

        return images
    
    except asyncio.TimeoutError:
        logging.error(f"Timeout while waiting for prompt {prompt_id} to complete.")
        raise

    except Exception as e:
        logging.error(f"An unexpected error occurred while getting images for prompt {prompt_id}: {e}")
        raise


def authenticate_user(domain, token):
    """Authenticates a user with a given domain and token."""
    try:
        if not domain or not token:
            raise ValueError("Domain and token must be provided for authentication")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = session.get(domain, headers=headers)
        response.raise_for_status()

        logging.info(f"Authentication successful with domain {domain}")
        return response.status_code, response.reason

    except ValueError as ve:
        logging.error(f"Authentication failed: {ve}")
        raise
    except requests.exceptions.RequestException as re:
        logging.error(f"Request error during authentication: {re}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during authentication: {e}")
        raise


def scene_description_template(textStyle, input_string, title):
    """Returns a random scene description from a predefined list."""
    list_scene = [
        """
            A breathtaking forest valley at sunrise, the scene filled with layers of lush greenery stretching into the distance, creating a sense of immense depth. The foreground features a narrow, winding trail lined with moss-covered stones and vibrant wildflowers in shades of yellow, blue, and white. Towering trees with textured bark and sprawling roots frame the edges of the trail, their leaves glowing in the soft golden light filtering through the canopy. Midground, a serene river winds through the valley, its surface glistening with reflections of the sky above, while a small wooden bridge arches gracefully over the water. In the background, rolling hills covered in dense forest rise into the mist, fading into subtle shades of blue and green. Overhead, the sky transitions from warm hues of orange and pink near the horizon to a crisp, pale blue, with a few fluffy clouds floating lazily. Birds soar in the distance, adding a sense of movement and life to the tranquil scene
        """,
        """
            A grand canyon landscape at sunrise, showcasing towering cliffs with intricate layers of red, orange, and brown rock. In the foreground, a rugged dirt trail winds along the edge of the canyon, dotted with desert shrubs and small cacti. Midground, the canyon descends into shadow, revealing a glimmering river far below that snakes through the valley, reflecting the soft golden light of the morning sun. The background features distant cliffs fading into pale hues of blue and purple, partially shrouded by mist. Overhead, the sky is painted in warm orange and pink tones, with streaks of soft clouds illuminated by the rising sun.
        """,
        """
            A pristine alpine lake surrounded by majestic snow-capped mountains under a clear morning sky. In the foreground, smooth pebbles line the crystal-clear water's edge, reflecting the sky and surrounding peaks. A wooden dock extends into the lake, with a small rowboat tied to it, creating a sense of stillness. Midground, the water mirrors the towering pine trees along the shoreline, their deep green contrasting with the icy blue of the lake. In the background, the rugged mountains rise sharply, their snow-covered peaks glowing softly in the early sunlight. Wisps of clouds cling to the highest ridges, adding texture to the sky.
        """,
        """
            A dramatic coastal cliffside at sunset, with jagged rocks plunging into the crashing waves of a deep blue ocean below. In the foreground, wild grasses and bright orange flowers cling to the rocky terrain, swaying in the salty breeze. Midground, a narrow dirt path winds along the cliff edge, leading to an old stone lighthouse perched at the highest point, its windows glowing faintly with warm light. In the background, the horizon stretches endlessly, with the ocean meeting the sky painted in gradients of pink, orange, and deep purple. Seagulls soar above, adding a sense of movement and life to the vast and serene scene.
        """,
        """
            A mystical forest scene at twilight, with towering trees forming a natural cathedral, their dense branches and leaves creating intricate patterns against the fading light. In the foreground, a moss-covered log lies across a bubbling creek, surrounded by glowing bioluminescent mushrooms and ferns. The midground reveals a clearing filled with wildflowers, their petals glowing faintly in shades of blue and white, while fireflies dance in the air. In the background, the forest stretches into darkness, with tall trees fading into the misty blue shadows. Rays of soft purple and golden light pierce through gaps in the canopy, adding an ethereal quality to the scene.
        """,
        """
            A serene meadow at dawn, bathed in the cool, soft light of sunrise. The meadow is alive with vibrant flowers in full bloom, featuring shades of lavender, blue, yellow, and white scattered across the lush, dew-covered grass. The sunlight filters through scattered trees at the edge of the meadow, casting gentle bluish shadows and illuminating the petals, making them glisten with morning dew. The sky is a tranquil gradient of light blue and teal, with thin, wispy clouds glowing faintly in the early morning light. In the foreground, tall wildflowers sway gently in the breeze, adding motion and life to the scene. A narrow dirt path winds through the field, leading toward a rustic wooden fence in the distance that separates the meadow from a grove of trees shrouded in a faint morning mist. The atmosphere is peaceful, refreshing, and bursting with natural beauty.
        """,
        """
            A serene meadow at dawn, bathed in the cool, soft light of sunrise. The sunlight filters through scattered trees at the edge of the meadow, casting gentle bluish shadows across the lush, dew-covered grass. Wildflowers in shades of pale blue, white, and soft lavender dot the meadow, adding subtle bursts of color. The sky is a tranquil gradient of light blue and teal, with thin, wispy clouds glowing faintly in the early morning light. In the foreground, tall grass sways gently in the breeze, with dew droplets sparkling like tiny crystals. A wooden bench sits at the edge of the meadow, inviting quiet reflection. In the distance, a rustic wooden fence separates the meadow from a grove of trees shrouded in a faint morning mist, completing the peaceful, cool-toned scene.
        """,
        """
            A serene meadow at dawn, bathed in the cool, soft light of sunrise. The sunlight filters through scattered trees at the edge of the meadow, casting gentle bluish shadows across the lush, dew-covered grass. Wildflowers in shades of pale blue, white, and soft lavender dot the meadow, adding subtle bursts of color. The sky is a tranquil gradient of light blue and teal, with thin, wispy clouds glowing faintly in the early morning light. In the foreground, tall grass sways gently in the breeze, with dew droplets sparkling like tiny crystals. A wooden bench sits at the edge of the meadow, where a person is seated, wrapped in a cozy sweater, holding a steaming cup of coffee. They appear calm and contemplative, gazing at the horizon as they enjoy the peaceful ambiance. In the distance, a rustic wooden fence separates the meadow from a grove of trees shrouded in a faint morning mist, completing the tranquil scene.
        """,
        """
            A serene meadow at dawn, bathed in the cool, soft light of sunrise. The sunlight filters through scattered trees at the edge of the meadow, casting gentle bluish shadows across the lush, dew-covered grass. Wildflowers in shades of pale blue, white, and soft lavender dot the meadow, adding subtle bursts of color. The sky is a tranquil gradient of light blue and teal, with thin, wispy clouds glowing faintly in the early morning light. In the foreground, a lone jogger is running along a dirt path that winds through the meadow, dressed in a lightweight hoodie and running shoes. Their breath forms faint clouds in the crisp air as they move with focus and energy. Tall grass sways gently in the breeze, and droplets of dew sparkle like tiny crystals. In the distance, a rustic wooden fence separates the meadow from a grove of trees shrouded in a faint morning mist, completing the peaceful yet invigorating scene.
        """,
        """
            A quiet alleyway at dawn, bathed in the soft, cool light of early morning. The sunlight streams gently into the alley from one side, casting long, soft shadows on the cobblestone path. The walls of the alley are adorned with faded pastel colors and ivy climbing up old brick buildings, with small windows reflecting the pale blue and golden hues of the morning sky. A lone bicycle leans against one wall, and a small wooden table with a potted plant sits near a doorway. The air feels fresh and tranquil, with a faint mist hovering close to the ground. In the distance, the alley opens up to reveal a glimpse of a city street just waking up, with a silhouette of a passerby carrying a bag. The scene captures the peaceful stillness of a city morning before the bustle begins.
        """,
        """
            A vibrant and festive Vietnamese Lunar New Year celebration captured in the Flux Lora art style, known for its fluid, luminous, and dynamic visuals. The scene showcases a bustling environment enriched with intricate details: traditional red lanterns suspended in mid-air, delicate peach blossoms in full bloom, and kumquat trees adorned with glistening golden fruits. In the foreground, people dressed in flowing, vividly colored áo dài (traditional Vietnamese attire) engage in heartwarming activities like presenting lì xì (red envelopes) to cheerful children and sharing traditional Tết delicacies.
        """
    ]

    return random.choice(list_scene)


def scene_template_1(textStyle, input_string, title, thumb_style):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """
    
    return f"""
        Scene Description:  
        {scene_description_template(textStyle, input_string, title)}

        Banner Title:  
        {textStyle} **"{title}"** in large, elegant lettering, {thumb_style}, positioned prominently at the top center of the image, blending seamlessly with the celebratory atmosphere.  

        Background Details:
        A lively village or urban setting, glowing with strings of festive lights, banners, and colorful decorations. Fireworks illuminate the twilight sky, adding a sense of wonder. Vibrant market stalls and close-knit family gatherings underscore the themes of community and tradition.  

        Color Palette:
        A harmonious blend of auspicious colors like radiant reds and gleaming golds, symbolizing luck and prosperity. These tones are complemented by soft pinks from peach blossoms, verdant greens of kumquat trees, and an ethereal glow from the lighting. The overall lighting is soft and immersive, exuding warmth and joy.  

        Composition:  
        The scene features a dynamic and balanced arrangement of cultural elements and animated interactions. Attention is given to the detailed textures of traditional clothing, the vibrant energy of decorations, and the genuine expressions of happiness, perfectly encapsulating the spirit of Vietnamese New Year celebrations. 
    """


def scene_template_2(textStyle, input_string, title):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """
    return f"""
        A moody lo-fi cityscape at night, bathed in shades of deep purple and black. The scene features a quiet urban alley with rain-slicked cobblestone streets reflecting the neon glow of purple and magenta signs mounted on old brick buildings. A single streetlamp casts a dim, cool light, creating long shadows and an air of mystery. In the foreground, a young person in a hoodie is leaning against a wall, headphones on, holding a steaming cup of coffee, their face softly illuminated by the glow of a nearby neon sign. A black cat with glowing purple eyes sits at their feet, adding an enigmatic vibe. In the background, silhouettes of distant skyscrapers with flickering purple windows fade into the night sky, where faint stars peek through. A soft rain falls, creating a rhythmic, tranquil atmosphere, with puddles scattered across the street glistening in the neon light. The entire scene exudes a chill, introspective lo-fi vibe.
    """


def scene_template_3(textStyle, input_string, title):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    return f"""
        ...
    """


def scene_template_4(textStyle, input_string, title):
    """_summary
        Function describe: This function is used to generate a scene template 2.
    """

    return f"""
        ...
    """


def create_prompt_and_call_api(input_string, title, thumb_style):
    """
        Creates a prompt and constructs the full API call prompt.
    """
    # Mapping of scene templates
    scene_templates = {
        1: scene_template_1,
        2: scene_template_1,
        3: scene_template_1,
        4: scene_template_1
    }

    # Randomly choose a scene template
    template_choice = random.choice([1, 2, 3, 4])
    scene_template = scene_templates[template_choice](TEXT_STYLE, input_string, title, thumb_style)

    # Construct and return the full API call prompt
    return f"```\n(({thumb_style})), ((detailed)), ((best quality))\n\n{scene_template}```"



async def logic_llm_option1(workflow, short_description, title, thumb_style, subfolder):
    """Implements Option 1 logic using Gemini AI."""
    workflow["59"]["inputs"]["text1"] = (
        f'describe "{short_description}" with {thumb_style} style as a prompt based on this exact format. '
        f'Banner title: {TEXT_STYLE} **"{title}"** in large, {thumb_style}, elegant lettering, positioned prominently at the top center of the image, blending seamlessly with the celebratory atmosphere.'
    )
    workflow["59"]["inputs"]["text2"] = create_prompt_and_call_api(short_description, title, thumb_style)

    if subfolder == SUBFOLDER_TOOL_RENDER:
        api_key_list = GEMINI_KEY_TOOL_RENDER
    elif subfolder == SUBFOLDER_TEAM_AUTOMATION:
        api_key_list = GEMINI_KEY_TEAM_AUTOMATION
    else:
        raise ValueError(f"Unsupported subfolder: {subfolder}")

    workflow["61"]["inputs"]["api_key"] = random.choice(api_key_list)
    return workflow


async def logic_llm_option2(workflow, short_description, title):
    """Implements Option 2 logic using Mistral LLM Model."""
    workflow["238"]["inputs"]["text"] = short_description

    if title == "":
        workflow["244"]["inputs"]["STRING"] = ""
    else:
        option1 = f'Banner title: {TEXT_STYLE} **"{title}"** in large, elegant lettering, positioned prominently at the center of the image.'
        option2 = f'Banner title: The future fonted title "{title}" is in neon, glowing, as if outlined by laser, exuding a sense of technology and a cold and mysterious atmosphere.'
        workflow["244"]["inputs"]["STRING"] = random.choice([option1, option2])

    return workflow


async def generate_images(short_description, title, thumbnail_number=1, thumb_style='realistic photo', subfolder='tool_render', filename_prefix='ytbthumb', lora_step=FLUX_LORA_STEP['tool_render']):
    """
        Generates images using the ComfyUI workflow via WebSocket.
    """

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
        if queue_count and (len(queue_count["queue_running"]) > 0 or len(queue_count["queue_pending"]) > 0):
            raise Exception(f'AI model is running another thumbnail images generation (Running: {len(queue_count["queue_running"])} Pending: {len(queue_count["queue_pending"])}). Please try again later.')

        with open("api-create-thumbnail-youtube-v3.json", "r", encoding="utf-8") as f:
            workflow_data = f.read()

        workflow = json.loads(workflow_data)
        noise_seed = random.randint(100000000000000, 1000000000000000)

        workflow["178"]["inputs"]["foldername_prefix"] = subfolder
        workflow["178"]["inputs"]["filename_prefix"] = filename_prefix
        
        # Thumbnail size setup
        workflow["29"]["inputs"]["width"] = THUMBNAIL_SIZES['fullhd']['original']['width']
        workflow["29"]["inputs"]["height"] = THUMBNAIL_SIZES['fullhd']['original']['height']
        workflow["29"]["inputs"]["batch_size"] = thumbnail_number
        workflow["76"]["inputs"]["width"] = THUMBNAIL_SIZES['fullhd']['scaled']['width']
        workflow["76"]["inputs"]["height"] = THUMBNAIL_SIZES['fullhd']['scaled']['height']

        workflow["17"]["inputs"]["steps"] = lora_step

        # Model 50  animal
        workflow["26"]["inputs"]["lora_name"] = "Children's illustrated story book.safetensors"
        workflow["26"]["inputs"]["strength_model"] = 1
        workflow["26"]["inputs"]["strength_clip"] = 1
        workflow["27"]["inputs"]["lora_name"] = "Round world chubby little animals doll toys.safetensors"

        # Model Poster Simple
        # workflow["26"]["inputs"]["lora_name"] = "flux.1_lora_flyway_Epic-detail_v2.safetensors"
        # workflow["26"]["inputs"]["strength_model"] = 0.2
        # workflow["26"]["inputs"]["strength_clip"] = 0.2
        # workflow["27"]["inputs"]["lora_name"] = "flux.1_lora_flyway_doodle-poster.safetensors"

        # Uncomment the desired option
        # workflow = await logic_llm_option1(workflow, short_description, title, thumb_style, subfolder)
        workflow = await logic_llm_option2(workflow, short_description, title)

        workflow["25"]["inputs"]["noise_seed"] = noise_seed

        images = await get_images(ws, workflow, noise_seed)
        return images

    except (ConnectionError, FileNotFoundError, ValueError) as e:
        raise e

    except Exception as e:
        logging.error(f"Unexpected error in generate_images: {e}")
        raise
    finally:
        if ws:
            try:
                ws.close()
            except Exception as e:
                logging.error(f"Error closing WebSocket: {e}")


def download_single_image(file_name: str, subfolder: str):
    """
        Downloads a single image from the server.
    """
    try:
        if not file_name or not subfolder:
            raise HTTPException(status_code=400, detail="Invalid file name or subfolder")

        file_path = FILE_DIRECTORY / subfolder / file_name

        if not file_path.resolve().is_relative_to(FILE_DIRECTORY.resolve()):
            raise HTTPException(status_code=400, detail="Invalid file path")

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Use send_file to send the file as a response
        return file_path

    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied to access the file")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File or directory not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
