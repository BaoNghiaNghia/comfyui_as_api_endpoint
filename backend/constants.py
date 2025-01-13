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
    # "AIzaSyCRZYMR_cqC5XdJ6wi4cO7Tch-knO_WtW4",
    # "AIzaSyBDi2wGNLiAD6iqncKZrGRZThKg_z-3I6c",
    # "AIzaSyCk9FrUaN_C9245Z_B3DvtzDggWu2ksCBg",
    # "AIzaSyBIX2kBeAS21wJUU05sJDB_0su1PiLJz_w",
    # "AIzaSyDetmj90xmAkybYuuMM4DXUc4Tc0hIRj-M",
    # "AIzaSyDP91xrK7B6zjnf0jKeRudguSUO-GHyhmQ",
    # "AIzaSyB8xGKrZBVfosfMIYnddX68hypfwZSY6dA",
    "AIzaSyDPNa--yBNIRGOkNKuNYU4tnVeDQsOVMSs"
]

GEMINI_KEY_TEAM_AUTOMATION = [
    # "AIzaSyDlO7yQAKhOafl6N5FT8O6dtMI3DKEROpg",
    # "AIzaSyDsvs2FqI213De7KH0sPYhCjgVcxDsJhAs",
    # "AIzaSyDQWtvW0-J88JhQ2-pkhRjMc1EGn0S0q-A",
    # "AIzaSyDI87mVYJ1yqUdBWguUPOpMS1U441YRtdA",
    # "AIzaSyCbFla1wYfzexbnwyd25jayJSM8IOlXWuc",
    # "AIzaSyAR7gTd2tu_y1XsGeTnVf1hZiv6BHs_CZA",
    # "AIzaSyAGuUI4P2PcUj5n8AOnbtVQHf4H8hbv4ZU",
    # "AIzaSyBq1C036iuzXp3f3EHrUU84b1fCP16xdpY",
    # "AIzaSyD0cry8PM9mSltSrvQxXwxWyvO4iYBi_ZA",
    # "AIzaSyDxaXcenPFLOIu39R7DIsbEo2tvMUAd_Bc",
    # "AIzaSyA3yKhWEcKxJ5YDLjONUjUkvDLB3mBQmfc",
    # "AIzaSyBxrbjQUL2cu5QLdRBkdp6pW9cv31FrrJA",
    # "AIzaSyDxaXcenPFLOIu39R7DIsbEo2tvMUAd_Bc",
    # "AIzaSyBxrbjQUL2cu5QLdRBkdp6pW9cv31FrrJA",
    # "AIzaSyDRPU-XEQzzX13AMKo_At0St0uqEQWAlqA",
    # "AIzaSyA85MP5jctMT9rKVR6gT16tEmsuO4JqpLg",
    # "AIzaSyCDzXlBfi5lRt2iLY5PT3NSodB-uVbcDuY",
    # "AIzaSyDJ2tjhP0xxDv7EJkJZwe0_g50qULOTDno",
    # "AIzaSyAV0LDFJk_ANuVW6ZHteJAUzF5U0Mq9BBE",
    "AIzaSyDPNa--yBNIRGOkNKuNYU4tnVeDQsOVMSs"
]

SUBFOLDER_TOOL_RENDER = 'tool_render'
SUBFOLDER_TEAM_AUTOMATION = 'team_automation'

MAX_IMAGES_THRESHOLD = 1500
COUNT_IMAGES_TO_DELETE = 5
FLUX_LORA_STEP = {
    'team_automation': 30,
    'tool_render': 25,
}

DEFAULT_FILENAME_PREFIX = 'ytbthumb'

CLIENT_ID = str(uuid.uuid4())

FILE_DIRECTORY = Path(os.getenv('OUTPUT_IMAGE_FOLDER', "/thumbnail_img"))

THUMBNAIL_PER_TIMES = 2

THUMBNAIL_SIZES = {
    'fullhd': {
        'original': {
            'width': 1280,
            'height': 720
        },
        'scaled': {
            'width': 1920,
            'height': 1080
        },
    },
    'rectangle': {
        'original': {
            'width': 1080,
            'height': 1080
        },
        'scaled': {
            'width': 1080,
            'height': 1080
        },
    },
}
INIT_REQUEST = [
    # {
    #     "short_description": [
    #         # "Young woman in wheat field at sunrise glow",
    #         "Young woman on sunlit beach, breeze flowing gently",
    #         # "Young woman jogging in park under bright sunlight",
    #         # "Young woman standing on cliff, ocean sunrise beauty",
    #         # "Young woman smiling in tulip field, holding bouquet",
    #         # "Young woman dancing joyfully in village, morning glow",
    #         "Young woman sipping coffee on cozy café windowsill",
    #         # "Young woman picking apples in sunny orchard, smiling",
    #         # "Young woman stretching arms freely on hilltop sunrise",
    #         # "Young woman relaxing in hammock, lush tropical garden",
    #         # "Young woman reflecting calmly by serene lake, sunlight",
    #         # "Young woman skipping along forest path, vibrant morning",
    #         # "Young woman laughing on grass with picnic in park",
    #         # "Young woman dancing under waterfall, glowing jungle sunrise",
    #         # "Young woman reading peacefully in café, bathed sunlight",
    #         # "Young woman walking in autumn forest, golden sunlight glow",
    #         # "Young woman relaxed on balcony overlooking lively sunny city",
    #         # "Young woman smiling by farmhouse, holding wildflowers brightly",
    #         # "Young woman standing near river, soft morning breeze flows",
    #         "Young woman embracing lavender field, glowing morning sun",
    #     ],
    #     "title": "Morning Music",
    #     "file_name": "morning_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "Narrow city alley with neon lights and a cat resting",  
    #         "Dark urban alley glowing with neon signs and a stray cat",  
    #         "City alley at night vibrant neon lights a cat walking by",  
    #         "Quiet alley bathed in neon hues a cat sitting calmly",  
    #         "Dimly lit alley with neon signs and a cat perched nearby",  
    #         "Rainy city alley with neon reflections and a wet cat",  
    #         "Deserted alley lined with neon-lit windows a cat lurking",  
    #         "Urban alley filled with neon signs a cat near food stalls",  
    #         "Futuristic alley with colorful neon lights and a curious cat",  
    #         "Misty alley glowing with neon a cat watching from shadows",  
    #         "Shadowy alley with vibrant neon signs a cat on the prowl",  
    #         "Rain-soaked alley reflecting neon lights a cat under a ledge",  
    #         "Lonely alley bathed in neon colors a cat exploring the night",  
    #         "Night alley with neon glow a cat beside vending machines",  
    #         "Modern city alley with neon-lit signs a cat crossing silently",  
    #         "Gritty urban alley with neon lights a cat hiding in mist",  
    #         "Silent alley with neon reflections a cat lounging on crates",  
    #         "Futuristic city alley with glowing neon ads a cat staring",  
    #         "Quiet neon alley at night a cat perched on a windowsill",  
    #         "Shadowed alley glowing in neon pinks a cat under soft rain",  
    #     ],
    #     "title": "Lofi Music",
    #     "file_name": "lofi_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "Rainforest, sunlight filtering, river winding gently",
    #         "Golden desert dunes, under vivid sunset",
    #         "Alpine meadow, wildflowers, towering snow peaks",
    #         "Misty jungle, hanging vines, cascading waterfall",
    #         "Crystal-clear beach, rugged cliffs, turquoise water",
    #         "Savanna sunrise, acacia trees, fiery sky",
    #         "Red canyon, layered rocks, winding river",
    #         "Ancient forest, towering redwoods, misty light",
    #         "Arctic landscape, floating icebergs, vivid aurora",
    #         "Tranquil lake, dense pines, vivid reflections",
    #         "Sharp peaks, swirling clouds, dramatic mountains",
    #         "Coral reef, colorful fish, sunlight below",
    #         "Tropical waterfall, lush forest, mist rising",
    #         "Rugged coastline, dramatic cliffs, crashing waves",
    #         "Still swamp, cypress trees, dark water",
    #         "Wildflowers hillside, deep blue sky",
    #         "Secluded valley, jagged peaks, meandering river",
    #         "Misty path, dense forest, mysterious journey",
    #         "Tropical island, pristine beaches, swaying palms",
    #         "Tundra landscape, wildflowers, distant snowy peaks",
    #         "Autumn forest, orange leaves, golden glow",
    #         "Glowing crystals, underground pool, deep cave",
    #         "Volcanic landscape, flowing lava, dark sky",
    #         "Mangrove forest, clear river, tranquil water",
    #         "Hillside terraces, rice paddies, shimmering sunlight",
    #         "Serene fjord, steep cliffs, snowy peaks",
    #         "Windswept moorland, blooming heather, solitary tree",
    #         "Icy glacier, mountain valley, shimmering sunlight",
    #         "Rainforest floor, vibrant fungi, glowing light",
    #     ],
    #     "title": "Deep Focus Music",
    #     "file_name": "deep_focus_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    {
        "short_description": [
            "Santa delivering presents under a snowy night with sparkling lights",
            "Musical instrument-shaped ornaments hanging on a Christmas tree",
            "A jazz band performing on stage surrounded by Christmas decor",
            "Santa playing a saxophone in falling snow",
            "Santa's sleigh flying across a starry sky with reindeer",
            "Santa checking his gift list in a cozy toy workshop",
            "A jazz duo performing at a Christmas market illuminated by fairy lights",
        ],
        "title": "Jazz Christmas",
        "file_name": "jazz_christmas",
        "day_of_week": [0,1,2,3,4,5,6],
    }
]


DATASET_TRAINED_FOLDER = Path(os.getenv('DATASET_TRAINED_FOLDER', "/dataset_trained"))

