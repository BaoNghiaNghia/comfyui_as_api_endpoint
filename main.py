import websocket  # websocket-client
import uuid
import json
import urllib.request
import urllib.parse
import random
from PIL import Image
import io
from termcolor import colored
from dotenv import load_dotenv
import os



# Step 1: Initialize the connection settings and load environment variables
print(colored("Step 1: Initialize the connection settings and load environment variables.", "cyan"))
print(colored("Loading configuration from the .env file.", "yellow"))
load_dotenv()



# Get server address from environment variable, default to "localhost:8188" if not set
server_address = os.getenv('COMFYUI_SERVER_ADDRESS', 'localhost:8188')
client_id = str(uuid.uuid4())



# Display the server address and client ID for transparency
print(colored(f"Server Address: {server_address}", "magenta"))
print(colored(f"Generated Client ID: {client_id}", "magenta"))
input(colored("Press Enter to continue...", "green"))



# Queue prompt function
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p, indent=4).encode('utf-8')  # Prettify JSON for print
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    
    # Step 5: Queue the prompt and prepare to send it to the ComfyUI server
    print(colored(f"Step 5: Queuing the prompt for client ID {client_id}.", "cyan"))
    input(colored("Press Enter to view the JSON that will be sent...", "green"))
    
    input(colored("Press Enter to continue and send the prompt...", "green"))
    
    return json.loads(urllib.request.urlopen(req).read())



# Get image function
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    
    print(colored(f"Fetching image from the server: {server_address}/view", "cyan"))
    print(colored(f"Filename: {filename}, Subfolder: {subfolder}, Type: {folder_type}", "yellow"))
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()



# Get history for a prompt ID
def get_history(prompt_id):
    print(colored(f"Fetching history for prompt ID: {prompt_id}.", "cyan"))
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())



# Get images from the workflow
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}

    last_reported_percentage = 0
    
    print(colored("Step 6: Start listening for progress updates via the WebSocket connection.", "cyan"))
    input(colored("Press Enter to continue...", "green"))

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'progress':
                data = message['data']
                current_progress = data['value']
                max_progress = data['max']
                percentage = int((current_progress / max_progress) * 100)

                # Only update progress every 10%
                if percentage >= last_reported_percentage + 10:
                    print(colored(f"Progress: {percentage}% in node {data['node']}", "yellow"))
                    last_reported_percentage = percentage

            elif message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print(colored("Execution complete.", "green"))
                    break  # Execution is done
        else:
            continue  # Previews are binary data

    # Fetch history and images after completion
    print(colored("Step 7: Fetch the history and download the images after execution completes.", "cyan"))
    input(colored("Press Enter to continue...", "green"))

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    print(colored(f"Downloading image: {image['filename']} from the server.", "yellow"))
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output

    return output_images



# Generate images function with customizable input
def generate_images():
    # Step 3: Establish WebSocket connection
    ws = websocket.WebSocket()
    ws_url = f"ws://{server_address}/ws?clientId={client_id}"
    print(colored(f"Step 3: Establishing WebSocket connection to {ws_url}", "cyan"))
    input(colored("Press Enter to continue...", "green"))
    ws.connect(ws_url)
    
    # Step 4: Load workflow from file and print it
    print(colored("Step 4: Loading the image generation workflow from 'workflow.json'.", "cyan"))
    with open("workflow.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    workflow["6"]["inputs"]["text"] = """
        ((Realistic photo)), ((perfect hand)), ((detailed)), ((best quality)), ((perfect tooth)), ((perfect eye))

        Scene Description:
        A vibrant and festive Vietnamese Lunar New Year celebration. The scene features a bustling environment with traditional decorations: red lanterns hanging in the air, peach blossoms in full bloom, and kumquat trees adorned with golden fruits. In the foreground, people in colorful áo dài (traditional Vietnamese attire) are smiling and engaging in joyous activities such as giving red envelopes (lì xì) to children and enjoying Tết delicacies.

        Background Details:
        A lively village or urban setting decorated with banners handwriter big text "Happy New Year" in top center, strings of lights, and fireworks lighting up the evening sky. Market stalls and family gatherings add a sense of community and tradition.

        Color Palette:
        Dominated by auspicious colors like red and gold, symbolizing luck and prosperity, with hints of pink from peach blossoms and green from the kumquat trees. The lighting is warm and inviting, emphasizing the celebratory mood.

        Composition:
        The layout has a balanced mix of cultural symbols and joyful interactions. Focus on the details of traditional clothing, decorations, and facial expressions to capture the essence of Vietnamese New Year traditions.
    """

    # Set a random seed for the KSampler node
    seed = random.randint(1, 1000000000000000)
    workflow["25"]["inputs"]["noise_seed"] = seed
    
    input(colored("Press Enter to continue...", "green"))

    # Fetch generated images
    images = get_images(ws, workflow)

    # Step 8: Close WebSocket connection after fetching the images
    print(colored(f"Step 8: Closing WebSocket connection to {ws_url}", "cyan"))
    ws.close()
    input(colored("Press Enter to continue...", "green"))

    return images, seed



if __name__ == "__main__":
    images, seed = generate_images()
