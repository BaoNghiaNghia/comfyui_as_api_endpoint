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
    "AIzaSyDmIPvKb7iTGglaBICwzR5BD0tWhD4UL2k",
    "AIzaSyBx2Q_qkWaxl_eQc1cjPQRkG5D-_sm2Yg4",
    "AIzaSyCQhpPnmtnLTcUNRp98ZXp8m3khcyyjp_Y",
    "AIzaSyBShFKq-s9T6UphIjrJhngBWjAdw9Osti8",
    "AIzaSyDmUx2fh466J9FIYFI6tCRIFSrEZLGXLaY",
    "AIzaSyB90zhWy91aD9QTIyHJa6jaY70apqnQfdw",
    "AIzaSyCB6MkXy2KOLYMvIc0ln1D3PvAtLB9LIbQ"
]

GEMINI_KEY_TEAM_AUTOMATION = [
    "AIzaSyA1Z5slGG7kbIOWinCnuz4OJiJ3a6G0t7Y",
    "AIzaSyC1KVctwhDdVbIDv2cOZDa1kWyz0gq_jOQ",
    "AIzaSyA85MP5jctMT9rKVR6gT16tEmsuO4JqpLg",
    "AIzaSyCzXVTqFDI1a1XV5iLwIAcqY-bjR1Xpz8Y",
    "AIzaSyChq25pUzIUTcIICrudPQi1rJiLHPjOCgA",
    "AIzaSyDUFE187efrejWYzHuK_uhidSIQL9G3Vzk",
    "AIzaSyBEpQWeTjyMAPdmWJ0Fqu61i6G54BbqbUo",
    "AIzaSyAbyGg-WXEmnHV6hYIbzU3hpshyIBfJp5k",
    "AIzaSyC7sF9TPticbbOJbo82yuuqGJyjIvTgFsk",
    "AIzaSyA4KM3KP2s1Wtf7WSK0Cf-UVK8DBHrDl84",
    "AIzaSyCjV7cuw7lm6RHenZl2SMPEOXXDSZhI5T8",
    "AIzaSyAO5XPik3WO225cp5vQXagi-BOmhjNkTzc",
    "AIzaSyCywQKy6D5E-yAzidTldWVhuPttZKKwM_Q",
    "AIzaSyDwTSVpdJ4nO5Ql9bnkpdEv4xMtnL_Hays",
    "AIzaSyBs_cp1hrXDYHmxHQufvqi9WhiLS8Iw_GE",
    "AIzaSyBNA_3L1JXOSn5s8NnfFRPXUTYYiEbreW0",
    "AIzaSyDBoL5qnSzGvNtjl0oOa3tWKvyJUcYypO0",
    "AIzaSyCrB_c2gN6zHRCfR5BtsebqpWEVlm4Byvc",
    "AIzaSyDmIPvKb7iTGglaBICwzR5BD0tWhD4UL2k",
    "AIzaSyBx2Q_qkWaxl_eQc1cjPQRkG5D-_sm2Yg4",
    "AIzaSyCQhpPnmtnLTcUNRp98ZXp8m3khcyyjp_Y",
    "AIzaSyBShFKq-s9T6UphIjrJhngBWjAdw9Osti8",
    "AIzaSyDmUx2fh466J9FIYFI6tCRIFSrEZLGXLaY",
    "AIzaSyB90zhWy91aD9QTIyHJa6jaY70apqnQfdw",
    "AIzaSyCB6MkXy2KOLYMvIc0ln1D3PvAtLB9LIbQ"
]

SUBFOLDER_TOOL_RENDER = 'tool_render'
SUBFOLDER_TEAM_AUTOMATION = 'team_automation'

MAX_IMAGES_THRESHOLD = 500
IMAGES_TO_DELETE = 5

DEFAULT_FILENAME_PREFIX = 'ytbthumb'

CLIENT_ID = str(uuid.uuid4())

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))