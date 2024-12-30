import uuid
import os
from pathlib import Path

# "realistic photo",
# "illustration",
# "cartoon",
# "comic",
# "dark",
# "water color",
# "pixel art",
# "surreal",
# "oil painting",
# "nature",
# "ink print",
# "pencil",
# "retrowave",
# "vintage japanese",
# "lifestyle",
# "collage",
# "glitchart",
# "retroglow",
# "lowkey cinematic",
# "analog memories",
# "trippy illustration",
# "fantasy cartoon",
# "pastel paint",
# "arcadebits",
# "squishy 3d",
# "product photography",
# "historical",
# "felted",
# "podium",
# "redveil",
# "darklight dreamscaped",
# "dreamlandscapes",
# "linework",
# "sonny anime",
# "soft pasty",
# "soft retro",
# "plushy world",
# "film effect",
# "anime",
# "warnand cold",
# "sparking",
# "blurry long exposure",
# "flutted glass",
# "glimmerish",
# "forties influence",
# "dadapop",
# "eighties movie",
# "renaissance fashion",
# "fineart",
# "neo classicart",
# "highend light",
# "anime",
# "3d colorful",
# "anime"


THUMBNAIL_STYLE_LIST = [
    "realistic photo",
    # "3d realistic",
    # "3d colorful"
]

GEMINI_KEY_TOOL_RENDER = [
    "AIzaSyCRZYMR_cqC5XdJ6wi4cO7Tch-knO_WtW4",
    "AIzaSyBDi2wGNLiAD6iqncKZrGRZThKg_z-3I6c",
    "AIzaSyCk9FrUaN_C9245Z_B3DvtzDggWu2ksCBg",
    "AIzaSyBIX2kBeAS21wJUU05sJDB_0su1PiLJz_w",
    "AIzaSyDetmj90xmAkybYuuMM4DXUc4Tc0hIRj-M",
    "AIzaSyDP91xrK7B6zjnf0jKeRudguSUO-GHyhmQ",
    "AIzaSyB8xGKrZBVfosfMIYnddX68hypfwZSY6dA"
]

GEMINI_KEY_TEAM_AUTOMATION = [
    "AIzaSyDlO7yQAKhOafl6N5FT8O6dtMI3DKEROpg",
    "AIzaSyDsvs2FqI213De7KH0sPYhCjgVcxDsJhAs",
    "AIzaSyDQWtvW0-J88JhQ2-pkhRjMc1EGn0S0q-A",
    "AIzaSyDI87mVYJ1yqUdBWguUPOpMS1U441YRtdA",
    "AIzaSyCbFla1wYfzexbnwyd25jayJSM8IOlXWuc",
    "AIzaSyAR7gTd2tu_y1XsGeTnVf1hZiv6BHs_CZA",
    "AIzaSyAGuUI4P2PcUj5n8AOnbtVQHf4H8hbv4ZU",
    "AIzaSyBq1C036iuzXp3f3EHrUU84b1fCP16xdpY",
    "AIzaSyD0cry8PM9mSltSrvQxXwxWyvO4iYBi_ZA",
    "AIzaSyDxaXcenPFLOIu39R7DIsbEo2tvMUAd_Bc",
    "AIzaSyA3yKhWEcKxJ5YDLjONUjUkvDLB3mBQmfc",
    "AIzaSyBxrbjQUL2cu5QLdRBkdp6pW9cv31FrrJA",
    "AIzaSyDxaXcenPFLOIu39R7DIsbEo2tvMUAd_Bc",
    "AIzaSyBxrbjQUL2cu5QLdRBkdp6pW9cv31FrrJA",
    "AIzaSyDRPU-XEQzzX13AMKo_At0St0uqEQWAlqA",
    "AIzaSyA85MP5jctMT9rKVR6gT16tEmsuO4JqpLg",
    "AIzaSyCDzXlBfi5lRt2iLY5PT3NSodB-uVbcDuY",
    "AIzaSyDJ2tjhP0xxDv7EJkJZwe0_g50qULOTDno",
    "AIzaSyAV0LDFJk_ANuVW6ZHteJAUzF5U0Mq9BBE",
]

SUBFOLDER_TOOL_RENDER = 'tool_render'
SUBFOLDER_TEAM_AUTOMATION = 'team_automation'

MAX_IMAGES_THRESHOLD = 500
IMAGES_TO_DELETE = 5

DEFAULT_FILENAME_PREFIX = 'ytbthumb'

CLIENT_ID = str(uuid.uuid4())

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))