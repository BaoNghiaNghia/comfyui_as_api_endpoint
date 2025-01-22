from ollama import chat
from ollama import ChatResponse

# response: ChatResponse = chat(model='llama3.2:3b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])

response: ChatResponse = chat(model='llama3.2-vision', messages=[
  {
    'role': 'user',
    'content': 'What is in this image?',
    'images': ['arctic_fox_music_30_108782538724425_1.jpg']
  },
])
print(response['message']['content'])