import base64
import requests
import asyncio
import json  # Importing the json module for safe JSON parsing

# Async function to call generate_image_caption
async def main():
    image_filename = 'holland_lop_rabbit_music_30_992076139481738_1.jpg'  # Image in the same directory
    
    try:
        # Read the image content and encode it to base64
        with open(image_filename, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
        
        # Send the POST request to the image captioning API
        response = requests.post("http://127.0.0.1:11434/api/chat", json={
            "model": 'llama3.2-vision',
            "messages": [
                {
                    "role": "user",
                    "content": "what is in this image?",
                    "images": [encoded_image]  # Use the base64-encoded image here
                }
            ]
        }, stream=True)  # Set stream=True to handle chunked responses
        
        # Check if the request was successful
        if response.status_code == 200:
            full_caption = ""
            # Iterate over each chunk of the response
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        # Parse the JSON chunk safely using json.loads
                        chunk_data = chunk.decode('utf-8')
                        message = json.loads(chunk_data)  # Safe JSON parsing
                        # Extract and concatenate the content from the message
                        full_caption += message['message']['content']
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing chunk: {e}")
            
            # Print the final concatenated caption
            return full_caption.strip()
        else:
            print(f"Failed to get a valid response. Status Code: {response.status_code}")
            print("Response Text:", response.text)
            return {"error": "Request failed", "status_code": response.status_code, "response_text": response.text}
    
    except requests.exceptions.RequestException as e:
        # Handle requests exceptions (e.g., network issues)
        print(f"An error occurred while making the request: {e}")
        return {"error": str(e)}

# Run the async main function
result = asyncio.run(main())
print("Final Result:", result)
