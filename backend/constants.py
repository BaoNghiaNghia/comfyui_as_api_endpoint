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

MAX_IMAGES_THRESHOLD = 2500
COUNT_IMAGES_TO_DELETE = 5
FLUX_LORA_STEP = {
    'team_automation': 30,
    'tool_render': 30,
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
            'width': 1200,
            'height': 1200
        },
        'scaled': {
            'width': 1500,
            'height': 1500
        },
    },
}
INIT_REQUEST = [
    # {
    #     "short_description": [
    #         "A capybara lying in the warm sun, eyes closed, wearing sunglasses, and looking completely relaxed, anime watercolor painting style",  
    #         "Capybara sitting by a shimmering lake, gazing into the distance while a gentle breeze ruffles its fur, anime watercolor painting style",  
    #         "Capybara munching on lush green grass in a peaceful garden, surrounded by blooming flowers, anime watercolor painting style",  
    #         "Capybara dozing under the shade of a tree, wearing a small hat and looking content, anime watercolor painting style",  
    #         "A group of capybaras playing together by a stream, splashing water joyfully and creating a lively atmosphere, anime watercolor painting style",  
    #         "Capybara lying back in a cool stream, water gently flowing around it, while small fish swim nearby, anime watercolor painting style",  
    #         "Capybara lounging on the sand, legs stretched out, wearing a beach hat, and soaking up the sun, anime watercolor painting style",  
    #         "Capybara scratching its ear with its hind leg, looking cute and whimsical as birds chirp in the background, anime watercolor painting style",  
    #         "Capybara swimming in a crystal-clear lake, creating gentle ripples as dragonflies hover above, anime watercolor painting style",  
    #         "Capybara gazing out over the water, surrounded by reeds, creating a dreamy, tranquil scene, anime watercolor painting style",  
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "capybara_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "A Scottish Fold cat curled up on a chair, wearing headphones, and purring softly in relaxation, anime watercolor painting style",  
    #         "Scottish Fold cat gazing out the window, sunlight highlighting its fur, as birds fly by, anime watercolor painting style",  
    #         "Scottish Fold cat playing with a ball of yarn, looking energetic and cute, with its tail flicking back and forth, anime watercolor painting style",  
    #         "Scottish Fold cat lying on its back, belly up, in an adorable sleeping pose, holding a tiny stuffed toy, anime watercolor painting style",  
    #         "Scottish Fold cat climbing a scratching post, wearing a tiny bowtie, looking curious and alert, anime watercolor painting style",  
    #         "Scottish Fold cat yawning widely, mouth open, and eyes closed, as if preparing for a long nap, anime watercolor painting style",  
    #         "Scottish Fold cat lying on a keyboard, looking sleepy and humorous, with a coffee mug next to it, anime watercolor painting style",  
    #         "Scottish Fold cat drinking water from a glass, gazing into the clear liquid and pawing at the rim, anime watercolor painting style",  
    #         "Scottish Fold cat wagging its tail, looking playful and joyful as it chases a laser pointer, anime watercolor painting style",  
    #         "Scottish Fold cat sleeping on a bookshelf, surrounded by old books, with a candle flickering nearby, anime watercolor painting style",  

    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "cat_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "A Shiba Inu running along the beach, fur blowing in the wind, wearing a bandana around its neck, anime watercolor painting style",  
    #         "Shiba Inu sitting next to its owner, eyes full of love and loyalty, with a leash resting nearby, anime watercolor painting style",  
    #         "Shiba Inu playing with its favorite toy, looking energetic and cute, as sand flies into the air, anime watercolor painting style",  
    #         "Shiba Inu digging in the sand, nose covered in sand, and barking excitedly at its discovery, anime watercolor painting style",  
    #         "Shiba Inu jumping up to greet its owner, wagging its tail and holding a frisbee in its mouth, anime watercolor painting style",  
    #         "Shiba Inu resting under the shade of a tree, wearing a cooling vest, and looking peaceful, anime watercolor painting style",  
    #         "Shiba Inu chewing on a bone, mouth full of bone and looking satisfied, while lying on a comfy blanket, anime watercolor painting style",  
    #         "Shiba Inu playing with fallen leaves, leaping through the air, with the autumn sun shining brightly, anime watercolor painting style",  
    #         "Shiba Inu staring intently at its food bowl, wearing a cute bib, eyes full of anticipation, anime watercolor painting style",
    #         "Shiba Inu chasing after a ball, running quickly and barking joyfully, with its ears perked up, anime watercolor painting style",  
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "shiba_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "A Holland Lop rabbit lying under the shade of a tree, wearing a flower crown, eyes closed, and fur soft, anime watercolor painting style",  
    #         "Holland Lop rabbit playing with leaves, hopping around energetically, while birds chirp in the background, anime watercolor painting style",  
    #         "Holland Lop rabbit jumping up and down, moving quickly and happily, with its ears flopping as it hops, anime watercolor painting style",  
    #         "Holland Lop rabbit nibbling on a carrot, wearing a tiny bow, and munching cutely while sitting in a basket, anime watercolor painting style",  
    #         "Holland Lop rabbit lying in the sun, legs stretched out, fur glowing as butterflies flutter nearby, anime watercolor painting style",  
    #         "Holland Lop rabbit scratching its ear with its hind leg, looking cute and whimsical under the dappled sunlight, anime watercolor painting style",  
    #         "Holland Lop rabbit hiding in a cardboard box, peeking out curiously, surrounded by scattered hay, anime watercolor painting style",  
    #         "Holland Lop rabbit hopping around the garden, wearing a tiny scarf, and exploring the small bushes, anime watercolor painting style",  
    #         "Holland Lop rabbit jumping over a small fence, legs pushing off the ground as it lands gracefully, anime watercolor painting style",  
    #         "Holland Lop rabbit sniffing a flower, nose touching the soft petals, with bees buzzing nearby, anime watercolor painting style",
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "rabbit_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # },
    # {
    #     "short_description": [
    #         "A Tawny owl perched on a tree branch, eyes wide and alert, anime watercolor painting style",
    #         "Tawny owl looking around with its big, round eyes, expression sharp and curious, anime watercolor painting style",
    #         "Tawny owl flying under the moonlight, wings wide and feathers smooth, anime watercolor painting style",
    #         "Tawny owl perched on a bookshelf, eyes bright and feathers soft, anime watercolor painting style",
    #         "Tawny owl looking downwards, eyes big and gaze sharp, anime watercolor painting style",
    #         "Tawny owl perched on a rooftop, wings spread and feathers glowing in the moonlight, anime watercolor painting style",
    #         "Tawny owl perched on top of a statue, eyes keen and sharp, anime watercolor painting style",
    #         "Tawny owl hooting at night, sound echoing and mysterious, anime watercolor painting style",
    #         "Tawny owl shaking its feathers after a bath, looking soft and smooth, anime watercolor painting style",
    #         "Tawny owl perched on an explorer's shoulder, eyes keen and full of curiosity, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "tawny_owl_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "An Emperor Penguin walking on ice, taking slow, steady steps, anime watercolor painting style",
    #         "Emperor Penguins playing together, creating a lively and joyful atmosphere, anime watercolor painting style",
    #         "Emperor Penguins standing in a long line, looking serious and united, anime watercolor painting style",
    #         "Emperor Penguin swimming underwater, wings stretched and body gliding smoothly, anime watercolor painting style",
    #         "Emperor Penguin caring for its egg, eyes full of responsibility and love, anime watercolor painting style",
    #         "Emperor Penguin standing and watching the sunrise, looking peaceful and serene, anime watercolor painting style",
    #         "Emperor Penguins lying together under the snow, feathers white and soft, anime watercolor painting style",
    #         "Emperor Penguin leaping out of the water, creating splashes of water droplets, anime watercolor painting style",
    #         "Emperor Penguin sitting on the beach, feathers shining under the sunlight, anime watercolor painting style",
    #         "Emperor Penguin sliding on its belly on the ice, looking cute and funny, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "emperor_penguin_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A Red Panda climbing a tree, claws gripping the branch and fur soft, anime watercolor painting style",
    #         "Red Panda playing with a branch, nibbling and pawing at it, anime watercolor painting style",
    #         "Red Panda jumping from branch to branch, moving quickly and gracefully, anime watercolor painting style",
    #         "Red Panda resting on a branch, eyes closed and fur glowing red, anime watercolor painting style",
    #         "Red Panda wrapping its tail around its face, looking cute and whimsical, anime watercolor painting style",
    #         "Red Panda chewing on bamboo, mouth munching softly and fur smooth, anime watercolor painting style",
    #         "Red Panda sitting near a bush, eyes curious and bright, anime watercolor painting style",
    #         "Red Panda playing with leaves, jumping through the yellow leaves, anime watercolor painting style",
    #         "Red Panda sleeping curled up, fur soft and warm, anime watercolor painting style",
    #         "Red Panda gazing at flowers from a branch, nose touching the soft petals, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "red_panda_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A Fennec Fox sleeping curled up in the sand, fur soft and warm, anime watercolor painting style",
    #         "Fennec Fox playing in the desert, running and jumping energetically, anime watercolor painting style",
    #         "Fennec Fox standing and looking into the distance, eyes bright and curious, anime watercolor painting style",
    #         "Fennec Fox shaking the sand off its fur, moving quickly and smoothly, anime watercolor painting style",
    #         "Fennec Fox digging a hole with its paws, nose full of sand and looking excited, anime watercolor painting style",
    #         "Fennec Fox lying under the shade of a tree, fur soft and eyes half-closed, anime watercolor painting style",
    #         "Fennec Fox sniffing a cactus flower, nose touching the soft petals, anime watercolor painting style",
    #         "Fennec Fox running and jumping under the moonlight, fur glowing and steps light, anime watercolor painting style",
    #         "Fennec Fox washing its face with its paws, looking cute and whimsical, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "fennec_fox_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A tall, pink flamingo standing gracefully on one leg in a serene pond at sunset, anime watercolor painting style",
    #         "Flamingo stretching its long neck and preening its feathers, surrounded by calm water, anime watercolor painting style",
    #         "Flamingo walking slowly through shallow water, its reflection shimmering on the surface, anime watercolor painting style",
    #         "Flamingo with its wings partially open, displaying a beautiful gradient of pink shades, anime watercolor painting style",
    #         "Flamingo standing in a group, creating a peaceful and social atmosphere, anime watercolor painting style",
    #         "Flamingo dipping its beak into the water to feed, ripples spreading out, anime watercolor painting style",
    #         "Flamingo standing in a gentle rain, droplets glistening on its feathers, anime watercolor painting style",
    #         "Flamingo resting with its head tucked under its wing, standing on one leg, anime watercolor painting style",
    #         "Flamingo taking a leisurely stroll along the edge of a lake, surrounded by reeds, anime watercolor painting style",
    #         "Flamingo looking at its reflection in the water, creating a tranquil and introspective scene, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "flamingo_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A small, playful corgi running through a field of tall grass, ears perked up, anime watercolor painting style",
    #         "Corgi sitting attentively, its tongue hanging out, and eyes full of joy, anime watercolor painting style",
    #         "Corgi lying on its back, paws in the air, and a blissful expression on its face, anime watercolor painting style",
    #         "Corgi chasing after a ball, mid-leap, with a determined look, anime watercolor painting style",
    #         "Corgi resting on a cozy blanket, surrounded by plush toys, anime watercolor painting style",
    #         "Corgi digging in the sand at the beach, nose covered in sand, anime watercolor painting style",
    #         "Corgi lying next to a fireplace, basking in the warm glow, anime watercolor painting style",
    #         "Corgi looking up at its owner with adoring eyes, tail wagging, anime watercolor painting style",
    #         "Corgi splashing in a shallow stream, droplets flying everywhere, anime watercolor painting style",
    #         "Corgi standing on a hill, looking out over a scenic landscape, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "corgi_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A friendly munchkin cat sitting on a windowsill, gazing curiously outside, anime watercolor painting style",
    #         "Munchkin cat playing with a string, its short legs moving rapidly, anime watercolor painting style",
    #         "Munchkin cat napping in a sunbeam, looking cozy and content, anime watercolor painting style",
    #         "Munchkin cat climbing up a scratching post, determined to reach the top, anime watercolor painting style",
    #         "Munchkin cat sitting with its front paws tucked under, looking like a fluffy loaf, anime watercolor painting style",
    #         "Munchkin cat chasing after a laser pointer, eyes wide with excitement, anime watercolor painting style",
    #         "Munchkin cat curled up in a ball, sleeping peacefully in a soft bed, anime watercolor painting style",
    #         "Munchkin cat peeking out from behind a curtain, looking playful and mischievous, anime watercolor painting style",
    #         "Munchkin cat playing with a ball of yarn, its paws skillfully maneuvering the string, anime watercolor painting style",
    #         "Munchkin cat sitting in a basket, looking up with a sweet and innocent expression, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "munchkin_cat_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A calm alpaca standing in a lush green field, its soft wool catching the sunlight, anime watercolor painting style",
    #         "Alpaca grazing peacefully, surrounded by wildflowers, anime watercolor painting style",
    #         "Alpaca lying down and chewing cud, looking relaxed and content, anime watercolor painting style",
    #         "Alpaca standing with other alpacas, creating a harmonious group scene, anime watercolor painting style",
    #         "Alpaca being sheared, its wool piled around it, anime watercolor painting style",
    #         "Alpaca with a colorful blanket draped over its back, adding a touch of whimsy, anime watercolor painting style",
    #         "Alpaca looking curiously at the camera, its big eyes full of gentleness, anime watercolor painting style",
    #         "Alpaca walking along a mountain trail, surrounded by breathtaking scenery, anime watercolor painting style",
    #         "Alpaca standing in the rain, water droplets glistening on its wool, anime watercolor painting style",
    #         "Alpaca playfully interacting with a baby alpaca, creating a heartwarming moment, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "alpaca_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A striking barn owl perched on a fence post, its heart-shaped face turned towards the camera, anime watercolor painting style",
    #         "Barn owl flying silently through a moonlit forest, wings spread wide, anime watercolor painting style",
    #         "Barn owl sitting in a barn loft, surrounded by hay bales and wooden beams, anime watercolor painting style",
    #         "Barn owl with its eyes closed, enjoying a moment of peace, anime watercolor painting style",
    #         "Barn owl standing on a branch, looking out over a misty field at dawn, anime watercolor painting style",
    #         "Barn owl swooping down towards the ground, hunting for prey, anime watercolor painting style",
    #         "Barn owl sitting with its wings slightly open, looking majestic and mysterious, anime watercolor painting style",
    #         "Barn owl perched on a weathered fence, with a soft orange glow from the setting sun, anime watercolor painting style",
    #         "Barn owl standing on a windowsill, its feathers ruffled by a gentle breeze, anime watercolor painting style",
    #         "Barn owl peeking out from a hollow tree, looking curious and alert, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "barn_owl_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A small arctic fox standing in the snow, its thick white fur blending perfectly with the surroundings, anime watercolor painting style",
    #         "Arctic fox curled up in a ball, sleeping soundly in a snowy den, anime watercolor painting style",
    #         "Arctic fox playing with a snowball, its playful nature shining through, anime watercolor painting style",
    #         "Arctic fox standing on a snow-covered rock, surveying its icy domain, anime watercolor painting style",
    #         "Arctic fox lying in the snow, eyes half-closed in contentment, anime watercolor painting style",
    #         "Arctic fox with its nose buried in the snow, searching for hidden treasures, anime watercolor painting style",
    #         "Arctic fox standing with its tail wrapped around its body for warmth, anime watercolor painting style",
    #         "Arctic fox walking gracefully through a snowy landscape, leaving delicate paw prints, anime watercolor painting style",
    #         "Arctic fox sitting and howling at the moon, creating a hauntingly beautiful scene, anime watercolor painting style",
    #         "Arctic fox chasing its tail in a snowy meadow, looking playful and energetic, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "arctic_fox_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A fluffy pomeranian sitting on a plush cushion, looking like a regal little lion, anime watercolor painting style",
    #         "Pomeranian playing with a squeaky toy, its mouth open in a joyful bark, anime watercolor painting style",
    #         "Pomeranian standing on its hind legs, begging for a treat with bright eyes, anime watercolor painting style",
    #         "Pomeranian curled up in a cozy dog bed, sleeping soundly, anime watercolor painting style",
    #         "Pomeranian running through a flower garden, fur bouncing with each step, anime watercolor painting style",
    #         "Pomeranian sitting in a basket, surrounded by colorful flowers, anime watercolor painting style",
    #         "Pomeranian standing proudly, with a small crown perched on its head, anime watercolor painting style",
    #         "Pomeranian lying on its back, enjoying a belly rub, anime watercolor painting style",
    #         "Pomeranian looking out the window, watching the world go by, anime watercolor painting style",
    #         "Pomeranian standing on a wooden deck, with the sunset casting a warm glow, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "pomeranian_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A luxurious persian cat sitting on a velvet cushion, looking regal and serene, anime watercolor painting style",
    #         "Persian cat grooming its long, silky fur, looking elegant and graceful, anime watercolor painting style",
    #         "Persian cat lying in a sunbeam, its fur glowing in the light, anime watercolor painting style",
    #         "Persian cat sitting on a windowsill, gazing out at the garden, anime watercolor painting style",
    #         "Persian cat playing with a feather toy, its eyes full of excitement, anime watercolor painting style",
    #         "Persian cat napping in a plush bed, looking utterly content, anime watercolor painting style",
    #         "Persian cat sitting with its paws tucked under, looking like a fluffy loaf, anime watercolor painting style",
    #         "Persian cat peeking out from behind a curtain, looking curious and playful, anime watercolor painting style",
    #         "Persian cat sitting on a bookshelf, surrounded by books and antiques, anime watercolor painting style",
    #         "Persian cat lying on a soft rug, its fur spread out like a luxurious blanket, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "persian_cat_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A majestic peacock displaying its colorful, iridescent tail feathers in full splendor, anime watercolor painting style",
    #         "Peacock walking gracefully through a garden, its tail trailing behind, anime watercolor painting style",
    #         "Peacock standing on a branch, its feathers catching the sunlight, anime watercolor painting style",
    #         "Peacock preening its feathers, looking elegant and serene, anime watercolor painting style",
    #         "Peacock standing in front of a temple, its vibrant colors contrasting with the stone, anime watercolor painting style",
    #         "Peacock with its tail feathers partially open, creating a beautiful fan shape, anime watercolor painting style",
    #         "Peacock walking through a field of wildflowers, its colors blending with the blooms, anime watercolor painting style",
    #         "Peacock standing in the rain, water droplets glistening on its feathers, anime watercolor painting style",
    #         "Peacock looking at its reflection in a pond, creating a tranquil scene, anime watercolor painting style",
    #         "Peacock standing on a hillside at sunset, its silhouette outlined against the sky, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "peacock_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A friendly husky running through the snow, eyes bright and tongue lolling, anime watercolor painting style",
    #         "Husky sitting attentively, with a look of intelligence and alertness, anime watercolor painting style",
    #         "Husky lying in front of a fireplace, basking in the warmth, anime watercolor painting style",
    #         "Husky playing with a snowball, its playful nature shining through, anime watercolor painting style",
    #         "Husky standing on a snowy hill, looking out over the landscape, anime watercolor painting style",
    #         "Husky howling at the moon, creating a hauntingly beautiful scene, anime watercolor painting style",
    #         "Husky lying in the snow, eyes half-closed in contentment, anime watercolor painting style",
    #         "Husky pulling a sled, muscles rippling with effort and determination, anime watercolor painting style",
    #         "Husky standing on a wooden deck, with the sun setting in the background, anime watercolor painting style",
    #         "Husky playing with other dogs in a snowy field, looking joyful and energetic, anime watercolor painting style."
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "husky_music",
    #     "day_of_week": [0,1,2,3,4,5,6]
    # },
    # {
    #     "short_description": [
    #         "A large ragdoll cat lying on its back, paws in the air, and looking completely relaxed, anime watercolor painting style",
    #         "Ragdoll cat sitting on a windowsill, gazing out at the garden with its blue eyes, anime watercolor painting style",
    #         "Ragdoll cat playing with a feather toy, its movements slow and graceful, anime watercolor painting style",
    #         "Ragdoll cat lying in a sunbeam, looking content and serene, anime watercolor painting style",
    #         "Ragdoll cat being held, its body limp and eyes half-closed in bliss, anime watercolor painting style",
    #         "Ragdoll cat sitting on a plush cushion, looking regal and elegant, anime watercolor painting style",
    #         "Ragdoll cat peeking out from behind a curtain, looking curious and playful, anime watercolor painting style",
    #         "Ragdoll cat sleeping in a cozy bed, surrounded by soft blankets, anime watercolor painting style",
    #         "Ragdoll cat playing with a ball of yarn, its paws skillfully maneuvering the string, anime watercolor painting style",
    #         "Ragdoll cat sitting on a bookshelf, surrounded by books and antiques, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "ragdoll_cat_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A large, colorful macaw parrot perched on a branch, its vibrant feathers catching the sunlight, anime watercolor painting style",
    #         "Macaw parrot spreading its wings, displaying an array of vivid colors, anime watercolor painting style",
    #         "Macaw parrot preening its feathers, showing off its intelligence and beauty, anime watercolor painting style",
    #         "Macaw parrot sitting on a wooden perch, looking inquisitively at the camera, anime watercolor painting style",
    #         "Macaw parrot interacting with other birds, creating a lively and social scene, anime watercolor painting style",
    #         "Macaw parrot eating from a bowl of tropical fruits, highlighting its playful nature, anime watercolor painting style",
    #         "Macaw parrot perched on a shoulder, showcasing its bond with humans, anime watercolor painting style",
    #         "Macaw parrot flying through a rainforest, wings wide and colors blending with the foliage, anime watercolor painting style",
    #         "Macaw parrot vocalizing, capturing its remarkable ability to mimic sounds, anime watercolor painting style",
    #         "Macaw parrot perched in a lush, green garden, surrounded by colorful flowers, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "macaw_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A stylish poodle standing elegantly, its curly coat perfectly groomed, anime watercolor painting style",
    #         "Poodle playing with a ball, its intelligence and agility on full display, anime watercolor painting style",
    #         "Poodle sitting attentively, its expressive eyes full of curiosity, anime watercolor painting style",
    #         "Poodle lying on a plush cushion, looking regal and sophisticated, anime watercolor painting style",
    #         "Poodle running through a park, its curly fur bouncing with each step, anime watercolor painting style",
    #         "Poodle being groomed, showcasing its elegant and well-kept appearance, anime watercolor painting style",
    #         "Poodle playing in the garden, surrounded by blooming flowers, anime watercolor painting style",
    #         "Poodle posing with a bow, emphasizing its refined and elegant nature, anime watercolor painting style",
    #         "Poodle lying next to a fireplace, enjoying the warmth and comfort, anime watercolor painting style",
    #         "Poodle standing on its hind legs, begging for a treat with bright eyes, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "poodle_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A playful sphynx cat sitting on a windowsill, its wrinkled skin catching the light, anime watercolor painting style",
    #         "Sphynx cat playing with a feather toy, its energy and curiosity evident, anime watercolor painting style",
    #         "Sphynx cat lying on a blanket, looking relaxed and content, anime watercolor painting style",
    #         "Sphynx cat sitting with its paws tucked under, showcasing its unique appearance, anime watercolor painting style",
    #         "Sphynx cat peeking out from under a cushion, its playful nature shining through, anime watercolor painting style",
    #         "Sphynx cat interacting with other pets, creating a warm and friendly atmosphere, anime watercolor painting style",
    #         "Sphynx cat basking in the sun, its skin glowing in the light, anime watercolor painting style",
    #         "Sphynx cat sleeping peacefully, wrapped in a soft blanket, anime watercolor painting style",
    #         "Sphynx cat sitting on a cozy rug, its eyes full of curiosity and intelligence, anime watercolor painting style",
    #         "Sphynx cat exploring a new environment, its adventurous spirit evident, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "sphynx_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A curious gentoo penguin standing on a rocky shore, its orange beak prominent, anime watercolor painting style",
    #         "Gentoo penguin waddling through the snow, its distinctive white stripe catching the eye, anime watercolor painting style",
    #         "Gentoo penguin swimming gracefully underwater, bubbles trailing behind, anime watercolor painting style",
    #         "Gentoo penguin interacting with its chick, showcasing strong parental bonds, anime watercolor painting style",
    #         "Gentoo penguin standing in a group, creating a social and lively scene, anime watercolor painting style",
    #         "Gentoo penguin resting on an iceberg, surrounded by a pristine icy landscape, anime watercolor painting style",
    #         "Gentoo penguin sliding on its belly across the ice, looking playful and energetic, anime watercolor painting style",
    #         "Gentoo penguin standing in the rain, water droplets glistening on its feathers, anime watercolor painting style",
    #         "Gentoo penguin looking out at the sea, creating a serene and contemplative scene, anime watercolor painting style",
    #         "Gentoo penguin jumping out of the water, showcasing its agility and grace, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "penguin_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A sleek dalmatian running through a field, its spotted coat contrasting with the green grass, anime watercolor painting style",
    #         "Dalmatian sitting attentively, its eyes full of energy and intelligence, anime watercolor painting style",
    #         "Dalmatian lying on a cozy rug, looking relaxed and content, anime watercolor painting style",
    #         "Dalmatian playing with a toy, its playful nature evident, anime watercolor painting style",
    #         "Dalmatian standing proudly, highlighting its association with firefighters, anime watercolor painting style",
    #         "Dalmatian running alongside its owner, showcasing its athleticism and energy, anime watercolor painting style",
    #         "Dalmatian resting under a tree, its spots standing out against the foliage, anime watercolor painting style",
    #         "Dalmatian interacting with other dogs, creating a lively and social atmosphere, anime watercolor painting style",
    #         "Dalmatian looking out the window, its eyes full of curiosity, anime watercolor painting style",
    #         "Dalmatian standing in front of a fire truck, highlighting its historical role, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "dalmatian_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A striking bengal cat lounging on a branch, its spotted coat blending with the surroundings, anime watercolor painting style",
    #         "Bengal cat playing with a feather toy, its wild and energetic nature on display, anime watercolor painting style",
    #         "Bengal cat sitting on a windowsill, gazing out at the garden with its piercing eyes, anime watercolor painting style",
    #         "Bengal cat climbing up a scratching post, showcasing its agility and strength, anime watercolor painting style",
    #         "Bengal cat lying in a sunbeam, its coat glowing with warmth, anime watercolor painting style",
    #         "Bengal cat interacting with other pets, creating a friendly and social scene, anime watercolor painting style",
    #         "Bengal cat exploring the garden, its eyes full of curiosity and excitement, anime watercolor painting style",
    #         "Bengal cat sitting on a shelf, surrounded by books and antiques, anime watercolor painting style",
    #         "Bengal cat grooming its coat, looking elegant and graceful, anime watercolor painting style",
    #         "Bengal cat playing in the grass, its wild spirit evident, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "bengal_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A small starling perched on a branch, its iridescent feathers catching the light, anime watercolor painting style",
    #         "Starling singing from a rooftop, showcasing its remarkable vocal ability, anime watercolor painting style",
    #         "Starling flying through the air, its wings spread wide, anime watercolor painting style",
    #         "Starling sitting with other birds, creating a social and lively scene, anime watercolor painting style",
    #         "Starling feeding in the garden, its bright eyes full of curiosity, anime watercolor painting style",
    #         "Starling perched on a fence, looking out at the world, anime watercolor painting style",
    #         "Starling playing in a birdbath, water droplets flying everywhere, anime watercolor painting style",
    #         "Starling sitting on a windowsill, its feathers glowing in the sunlight, anime watercolor painting style",
    #         "Starling singing at dawn, creating a beautiful and serene atmosphere, anime watercolor painting style",
    #         "Starling interacting with its mate, showcasing its social nature, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "starling_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A small chihuahua sitting on a cushion, looking regal and confident, anime watercolor painting style",
    #         "Chihuahua playing with a squeaky toy, its big personality shining through, anime watercolor painting style",
    #         "Chihuahua lying on its back, paws in the air, looking blissful, anime watercolor painting style",
    #         "Chihuahua sitting attentively, its ears perked up and eyes bright, anime watercolor painting style",
    #         "Chihuahua running through the grass, its tiny legs moving quickly, anime watercolor painting style",
    #         "Chihuahua resting in a cozy bed, surrounded by soft blankets, anime watercolor painting style",
    #         "Chihuahua standing proudly, showcasing its big personality, anime watercolor painting style",
    #         "Chihuahua interacting with other pets, creating a friendly and social scene, anime watercolor painting style",
    #         "Chihuahua looking up at its owner, eyes full of devotion, anime watercolor painting style",
    #         "Chihuahua exploring the garden, its curious nature evident, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "chihuahua_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A large maine coon cat lying on a windowsill, its long, bushy tail draped over the edge, anime watercolor painting style",
    #         "Maine coon cat playing with a toy mouse, its movements slow and deliberate, anime watercolor painting style",
    #         "Maine coon cat sitting on a shelf, surrounded by books and antiques, anime watercolor painting style",
    #         "Maine coon cat lounging in a sunbeam, its fur glowing with warmth, anime watercolor painting style",
    #         "Maine coon cat grooming its long fur, looking elegant and graceful, anime watercolor painting style",
    #         "Maine coon cat interacting with other pets, creating a friendly and social scene, anime watercolor painting style",
    #         "Maine coon cat sitting on a tree branch, its eyes full of curiosity, anime watercolor painting style",
    #         "Maine coon cat exploring the garden, its movements slow and deliberate, anime watercolor painting style",
    #         "Maine coon cat lying on a cozy rug, looking relaxed and content, anime watercolor painting style",
    #         "Maine coon cat playing with a feather toy, its playful nature evident, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "maine_coon_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A majestic bald eagle perched on a branch, its white head standing out against the sky, anime watercolor painting style",
    #         "Bald eagle flying through the air, its wings spread wide and powerful, anime watercolor painting style",
    #         "Bald eagle sitting on a rock, looking out over a vast landscape, anime watercolor painting style",
    #         "Bald eagle interacting with its chick, showcasing strong parental bonds, anime watercolor painting style",
    #         "Bald eagle perched on a high cliff, creating a dramatic and awe-inspiring scene, anime watercolor painting style",
    #         "Bald eagle swooping down towards the water, talons extended, anime watercolor painting style",
    #         "Bald eagle sitting in a tree, its eyes full of intensity and focus, anime watercolor painting style",
    #         "Bald eagle flying through a stormy sky, showcasing its resilience and strength, anime watercolor painting style",
    #         "Bald eagle standing proudly, highlighting its role as a national symbol, anime watercolor painting style",
    #         "Bald eagle perched on a branch at sunrise, creating a serene and majestic atmosphere, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "bald_eagle_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A fluffy samoyed lying in the snow, its white fur blending with the surroundings, anime watercolor painting style",
    #         "Samoyed playing with a toy, its joyful and playful nature evident, anime watercolor painting style",
    #         "Samoyed sitting attentively, its bright eyes full of intelligence, anime watercolor painting style",
    #         "Samoyed running through a field, its fur bouncing with each step, anime watercolor painting style",
    #         "Samoyed lying in front of a fireplace, enjoying the warmth and comfort, anime watercolor painting style",
    #         "Samoyed interacting with other dogs, creating a lively and social scene, anime watercolor painting style",
    #         "Samoyed exploring the garden, its curious nature on full display, anime watercolor painting style",
    #         "Samoyed standing proudly, showcasing its gentle and friendly personality, anime watercolor painting style",
    #         "Samoyed sitting with its tongue hanging out, looking happy and relaxed, anime watercolor painting style",
    #         "Samoyed playing in the snow, creating a joyful and energetic scene, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "samoyed_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A small cockatiel perched on a branch, its bright crest standing out against a pastel background, anime watercolor painting style",
    #         "Cockatiel singing happily, its melodious chirp creating a serene atmosphere, anime watercolor painting style",
    #         "Cockatiel playing with a bell toy, showcasing its playful nature, anime watercolor painting style",
    #         "Cockatiel preening its feathers, looking elegant and calm, anime watercolor painting style",
    #         "Cockatiel interacting with other birds, creating a social scene, anime watercolor painting style",
    #         "Cockatiel perched on a windowsill, bathed in warm sunlight, anime watercolor painting style",
    #         "Cockatiel exploring a cozy room, its eyes full of curiosity, anime watercolor painting style",
    #         "Cockatiel sitting on a shoulder, showing a bond with its owner, anime watercolor painting style",
    #         "Cockatiel enjoying a bath in a shallow dish, splashing water around, anime watercolor painting style",
    #         "Cockatiel perched on a colorful perch, surrounded by houseplants, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "cockatiel_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A playful sea otter floating on its back in calm waters, holding a shell, anime watercolor painting style",
    #         "Sea otter cracking open a shell on its belly, looking content, anime watercolor painting style",
    #         "Sea otter swimming gracefully underwater, bubbles trailing behind, anime watercolor painting style",
    #         "Sea otter resting on a rock, eyes half-closed in relaxation, anime watercolor painting style",
    #         "Sea otter interacting with another otter, showcasing social behavior, anime watercolor painting style",
    #         "Sea otter playing with a ball, its playful nature evident, anime watercolor painting style",
    #         "Sea otter grooming its fur, looking clean and fluffy, anime watercolor painting style",
    #         "Sea otter lounging on a beach, surrounded by seashells, anime watercolor painting style",
    #         "Sea otter diving into the water, creating a splash, anime watercolor painting style",
    #         "Sea otter basking in the sunlight, with water glistening on its fur, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "sea_otter_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A stunning white peacock displaying its elegant tail feathers in full splendor, anime watercolor painting style",
    #         "White peacock standing gracefully in a lush garden, feathers glowing in the sunlight, anime watercolor painting style",
    #         "White peacock preening its feathers, looking regal and serene, anime watercolor painting style",
    #         "White peacock walking through a field of wildflowers, its purity symbolized by the setting, anime watercolor painting style",
    #         "White peacock standing in front of a grand palace, adding a touch of elegance, anime watercolor painting style",
    #         "White peacock with its tail feathers partially open, creating a beautiful fan shape, anime watercolor painting style",
    #         "White peacock resting in a shaded area, looking tranquil and majestic, anime watercolor painting style",
    #         "White peacock interacting with other birds, showcasing its social nature, anime watercolor painting style",
    #         "White peacock walking beside a clear pond, its reflection shimmering on the water, anime watercolor painting style",
    #         "White peacock perched on a branch, with its stunning feathers cascading down, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "white_peacock_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A large sulcata tortoise slowly walking through a grassy field, its shell catching the sunlight, anime watercolor painting style",
    #         "Sulcata tortoise munching on fresh greens, looking content and relaxed, anime watercolor painting style",
    #         "Sulcata tortoise resting under the shade of a tree, its longevity symbolized by the setting, anime watercolor painting style",
    #         "Sulcata tortoise interacting with other tortoises, showcasing its resilience, anime watercolor painting style",
    #         "Sulcata tortoise exploring a sandy desert, its shell blending with the surroundings, anime watercolor painting style",
    #         "Sulcata tortoise basking in the sun, with sand gently falling off its shell, anime watercolor painting style",
    #         "Sulcata tortoise digging a burrow, showcasing its natural behavior, anime watercolor painting style",
    #         "Sulcata tortoise walking along a rocky path, its determined steps evident, anime watercolor painting style",
    #         "Sulcata tortoise resting in a calm and serene garden, surrounded by flowers, anime watercolor painting style",
    #         "Sulcata tortoise lying in a shallow pond, cooling off on a warm day, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "sulcata_tortoise_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A sleek seal lounging on a sandy beach, looking relaxed and at ease, anime watercolor painting style",
    #         "Seal swimming gracefully underwater, its streamlined body moving effortlessly, anime watercolor painting style",
    #         "Seal playing with a fish, showcasing its playful nature, anime watercolor painting style",
    #         "Seal resting on a rock, surrounded by gentle waves, anime watercolor painting style",
    #         "Seal interacting with other seals, creating a social and lively scene, anime watercolor painting style",
    #         "Seal basking in the sunlight, with droplets of water glistening on its fur, anime watercolor painting style",
    #         "Seal diving into the ocean, creating a splash, anime watercolor painting style",
    #         "Seal popping its head out of the water, looking curious, anime watercolor painting style",
    #         "Seal rolling in the sand, enjoying a moment of playfulness, anime watercolor painting style",
    #         "Seal sitting on a beach at sunset, creating a serene and picturesque scene, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "seal_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A curious ferret peeking out from a cozy blanket, its eyes full of mischief, anime watercolor painting style",
    #         "Ferret playing with a ball, its playful nature on full display, anime watercolor painting style",
    #         "Ferret exploring a room, looking for hidden treasures, anime watercolor painting style",
    #         "Ferret lying on its back, enjoying a gentle belly rub, anime watercolor painting style",
    #         "Ferret interacting with other pets, creating a lively and social scene, anime watercolor painting style",
    #         "Ferret running through a tube, showcasing its energetic behavior, anime watercolor painting style",
    #         "Ferret lounging in a hammock, looking completely relaxed, anime watercolor painting style",
    #         "Ferret chasing after a toy, its movements quick and agile, anime watercolor painting style",
    #         "Ferret sitting in a basket, surrounded by soft blankets, anime watercolor painting style",
    #         "Ferret playing hide-and-seek, popping its head out from behind a cushion, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "ferret_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A wide-eyed burrowing owl peeking out from its underground burrow, anime watercolor painting style",
    #         "Burrowing owl sitting on a fence post, looking alert and watchful, anime watercolor painting style",
    #         "Burrowing owl flying low over the ground, wings spread wide, anime watercolor painting style",
    #         "Burrowing owl perched on a rock, with its burrow entrance in the background, anime watercolor painting style",
    #         "Burrowing owl interacting with its mate, showcasing its social behavior, anime watercolor painting style",
    #         "Burrowing owl standing on one leg, looking contemplative, anime watercolor painting style",
    #         "Burrowing owl hunting in a grassy field, its keen eyesight evident, anime watercolor painting style",
    #         "Burrowing owl resting in its burrow, with only its head visible, anime watercolor painting style",
    #         "Burrowing owl standing at the entrance of its burrow, with the sunset casting a warm glow, anime watercolor painting style",
    #         "Burrowing owl perched on a branch, looking out over the landscape with wide eyes, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "owl_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A powerful Akita Inu standing proudly, its coat shining in the sunlight, anime watercolor painting style",
    #         "Akita Inu running through a snow-covered field, its strong build evident, anime watercolor painting style",
    #         "Akita Inu sitting attentively, with a look of loyalty and dignity, anime watercolor painting style",
    #         "Akita Inu interacting with its owner, showcasing a strong bond, anime watercolor painting style",
    #         "Akita Inu lying on a porch, looking relaxed and watchful, anime watercolor painting style",
    #         "Akita Inu playing with a toy, its playful side shining through, anime watercolor painting style",
    #         "Akita Inu standing on a hill, looking out over the landscape, anime watercolor painting style",
    #         "Akita Inu resting under a tree, its coat blending with the surroundings, anime watercolor painting style",
    #         "Akita Inu walking through a forest, its steps confident and deliberate, anime watercolor painting style",
    #         "Akita Inu standing in front of a traditional Japanese house, highlighting its heritage, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "akita_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A docile highland cow standing in a green pasture, its long, shaggy hair catching the wind, anime watercolor painting style",
    #         "Highland cow grazing peacefully, surrounded by wildflowers, anime watercolor painting style",
    #         "Highland cow lying down in a meadow, looking calm and serene, anime watercolor painting style",
    #         "Highland cow interacting with other cows, showcasing a social scene, anime watercolor painting style",
    #         "Highland cow standing on a hillside, with the Scottish landscape in the background, anime watercolor painting style",
    #         "Highland cow being petted by a child, highlighting its gentle nature, anime watercolor painting style",
    #         "Highland cow walking along a dirt path, its long hair swaying with each step, anime watercolor painting style",
    #         "Highland cow resting under the shade of a tree, looking relaxed, anime watercolor painting style",
    #         "Highland cow standing in front of a traditional Scottish cottage, adding a rustic charm, anime watercolor painting style",
    #         "Highland cow basking in the warm sunlight, with its hair glowing, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "cow_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A nocturnal kiwi bird foraging in the underbrush, its long beak searching the ground, anime watercolor painting style",
    #         "Kiwi bird nestled among ferns and leaves, its small eyes shining in the moonlight, anime watercolor painting style",
    #         "Kiwi bird walking through a forest at dusk, with soft light filtering through the trees, anime watercolor painting style",
    #         "Kiwi bird hiding in tall grass, only its long beak visible, anime watercolor painting style",
    #         "Kiwi bird interacting with another kiwi, showcasing its social behavior, anime watercolor painting style",
    #         "Kiwi bird standing by a stream, with its reflection visible in the water, anime watercolor painting style",
    #         "Kiwi bird exploring a mossy forest floor, its beak probing the earth, anime watercolor painting style",
    #         "Kiwi bird resting in a hollow log, looking cozy and hidden, anime watercolor painting style",
    #         "Kiwi bird standing on a rocky outcrop, illuminated by the first light of dawn, anime watercolor painting style",
    #         "Kiwi bird sniffing around a pile of fallen leaves, creating a natural and peaceful scene, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "kiwi_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A majestic white Bengal tiger walking through a dense jungle, its white coat standing out against the greenery, anime watercolor painting style",
    #         "White Bengal tiger lying on a rock, basking in the warm sunlight, anime watercolor painting style",
    #         "White Bengal tiger prowling through tall grass, its powerful muscles rippling, anime watercolor painting style",
    #         "White Bengal tiger looking directly at the camera, its blue eyes piercing and intense, anime watercolor painting style",
    #         "White Bengal tiger resting by a waterfall, with water cascading in the background, anime watercolor painting style",
    #         "White Bengal tiger playing with a cub, showcasing its nurturing side, anime watercolor painting style",
    #         "White Bengal tiger drinking from a clear river, its reflection mirrored in the water, anime watercolor painting style",
    #         "White Bengal tiger standing on a cliff, looking out over its territory, anime watercolor painting style",
    #         "White Bengal tiger sitting under the shade of a large tree, looking relaxed and regal, anime watercolor painting style",
    #         "White Bengal tiger walking through a snowy landscape, blending seamlessly with the surroundings, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "tiger_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A vibrant betta fish swimming gracefully in a clear aquarium, its long fins flowing behind, anime watercolor painting style",
    #         "Betta fish interacting with aquatic plants, creating a colorful underwater scene, anime watercolor painting style",
    #         "Betta fish flaring its fins in a display of territorial behavior, anime watercolor painting style",
    #         "Betta fish resting on a leaf, looking serene and beautiful, anime watercolor painting style",
    #         "Betta fish swimming among bubbles, adding a dynamic touch to the scene, anime watercolor painting style",
    #         "Betta fish showing off its vivid colors under a bright light, anime watercolor painting style",
    #         "Betta fish swimming in a tank decorated with colorful rocks and plants, anime watercolor painting style",
    #         "Betta fish interacting with other fish, showcasing its social behavior, anime watercolor painting style",
    #         "Betta fish creating a bubble nest at the surface of the water, anime watercolor painting style",
    #         "Betta fish swimming in a calm, dimly-lit aquarium, creating a relaxing atmosphere, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "betta_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A large coconut crab climbing a tree, its powerful claws gripping the bark, anime watercolor painting style",
    #         "Coconut crab cracking open a coconut, showcasing its strength, anime watercolor painting style",
    #         "Coconut crab exploring a sandy beach, with the ocean in the background, anime watercolor painting style",
    #         "Coconut crab hiding in a rock crevice, only its claws visible, anime watercolor painting style",
    #         "Coconut crab interacting with other crabs, creating a lively scene, anime watercolor painting style",
    #         "Coconut crab carrying a coconut, moving slowly across the sand, anime watercolor painting style",
    #         "Coconut crab resting under a palm tree, looking relaxed and content, anime watercolor painting style",
    #         "Coconut crab standing on a rocky outcrop, with waves crashing below, anime watercolor painting style",
    #         "Coconut crab digging a burrow in the sand, showcasing its natural behavior, anime watercolor painting style",
    #         "Coconut crab basking in the sunlight, with its shell glistening, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "coconut_crab_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "An elegant Turkish Angora cat sitting gracefully on a windowsill, its silky coat glowing in the sunlight, anime watercolor painting style",
    #         "Turkish Angora cat playing with a feather toy, its playful nature evident, anime watercolor painting style",
    #         "Turkish Angora cat lying in a sunbeam, looking relaxed and content, anime watercolor painting style",
    #         "Turkish Angora cat grooming its long fur, looking elegant and serene, anime watercolor painting style",
    #         "Turkish Angora cat sitting with its paws tucked under, looking like a fluffy cloud, anime watercolor painting style",
    #         "Turkish Angora cat interacting with other pets, creating a friendly scene, anime watercolor painting style",
    #         "Turkish Angora cat exploring a garden, its eyes full of curiosity, anime watercolor painting style",
    #         "Turkish Angora cat sitting on a plush cushion, looking regal and sophisticated, anime watercolor painting style",
    #         "Turkish Angora cat peeking out from behind a curtain, looking playful and mischievous, anime watercolor painting style",
    #         "Turkish Angora cat lying on a cozy rug, its fur spread out like a luxurious blanket, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "turkish_angora_cat_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "An intelligent Border Collie herding sheep in a green pasture, showcasing its agility and skill, anime watercolor painting style",
    #         "Border Collie sitting attentively, its eyes full of focus and determination, anime watercolor painting style",
    #         "Border Collie running through a field, its fur flowing in the wind, anime watercolor painting style",
    #         "Border Collie playing with a frisbee, its playful nature evident, anime watercolor painting style",
    #         "Border Collie lying on a porch, looking relaxed and content, anime watercolor painting style",
    #         "Border Collie interacting with its owner, showcasing a strong bond, anime watercolor painting style",
    #         "Border Collie exploring a forest, its keen senses on full alert, anime watercolor painting style",
    #         "Border Collie sitting proudly with a flock of sheep in the background, anime watercolor painting style",
    #         "Border Collie resting under a tree, looking calm and serene, anime watercolor painting style",
    #         "Border Collie standing on a hill, looking out over the landscape, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "border_collie_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A cute Lionhead Rabbit sitting in a field of wildflowers, its mane of fur blowing in the breeze, anime watercolor painting style",
    #         "Lionhead Rabbit playing with a ball, its playful nature evident, anime watercolor painting style",
    #         "Lionhead Rabbit lying in a sunbeam, looking relaxed and content, anime watercolor painting style",
    #         "Lionhead Rabbit grooming its fur, looking elegant and serene, anime watercolor painting style",
    #         "Lionhead Rabbit exploring a garden, its eyes full of curiosity, anime watercolor painting style",
    #         "Lionhead Rabbit interacting with other rabbits, creating a friendly scene, anime watercolor painting style",
    #         "Lionhead Rabbit sitting in a cozy nest of hay, looking comfortable and warm, anime watercolor painting style",
    #         "Lionhead Rabbit peeking out from behind a bush, looking playful and mischievous, anime watercolor painting style",
    #         "Lionhead Rabbit hopping through a meadow, its mane of fur bouncing with each step, anime watercolor painting style",
    #         "Lionhead Rabbit resting under a tree, looking calm and peaceful, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "lionhead_rabbit_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A small starling perched on a branch, its iridescent feathers catching the light, anime watercolor painting style",
    #         "Starling singing from a rooftop, showcasing its remarkable vocal ability, anime watercolor painting style",
    #         "Starling flying through the air, its wings spread wide, anime watercolor painting style",
    #         "Starling sitting with other birds, creating a social and lively scene, anime watercolor painting style",
    #         "Starling feeding in the garden, its bright eyes full of curiosity, anime watercolor painting style",
    #         "Starling perched on a fence, looking out at the world, anime watercolor painting style",
    #         "Starling playing in a birdbath, water droplets flying everywhere, anime watercolor painting style",
    #         "Starling sitting on a windowsill, its feathers glowing in the sunlight, anime watercolor painting style",
    #         "Starling singing at dawn, creating a beautiful and serene atmosphere, anime watercolor painting style",
    #         "Starling interacting with its mate, showcasing its social nature, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "common_starling_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A small, intelligent pig standing in a garden, its curious eyes shining, anime watercolor painting style",
    #         "small pig playing with a ball, its playful nature evident, anime watercolor painting style",
    #         "small pig lying in a cozy bed, looking relaxed and content, anime watercolor painting style",
    #         "small pig exploring a yard, its nose sniffing the ground, anime watercolor painting style",
    #         "small pig interacting with other pets, creating a friendly scene, anime watercolor painting style",
    #         "small pig standing on a porch, its tail wagging with excitement, anime watercolor painting style",
    #         "small pig resting under a tree, looking calm and serene, anime watercolor painting style",
    #         "small pig digging in the dirt, showcasing its natural behavior, anime watercolor painting style",
    #         "small pig sitting next to its owner, highlighting its bond with humans, anime watercolor painting style",
    #         "small pig playing in the mud, looking joyful and carefree, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "small_pig_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A playful bottlenose dolphin leaping out of the water, creating a splash, anime watercolor painting style",
    #         "Bottlenose dolphin swimming gracefully underwater, its streamlined body moving effortlessly, anime watercolor painting style",
    #         "Bottlenose dolphin interacting with other dolphins, showcasing its social behavior, anime watercolor painting style",
    #         "Bottlenose dolphin playing with a ball, its playful nature evident, anime watercolor painting style",
    #         "Bottlenose dolphin jumping through a hoop, highlighting its intelligence, anime watercolor painting style",
    #         "Bottlenose dolphin resting on the surface of the water, looking relaxed, anime watercolor painting style",
    #         "Bottlenose dolphin interacting with humans, showcasing its friendly nature, anime watercolor painting style",
    #         "Bottlenose dolphin diving deep into the ocean, creating bubbles, anime watercolor painting style",
    #         "Bottlenose dolphin swimming alongside a boat, creating a dynamic scene, anime watercolor painting style",
    #         "Bottlenose dolphin basking in the sunlight, with water glistening on its skin, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "bottlenose_dolphin_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    # {
    #     "short_description": [
    #         "A fluffy polar bear cub playing in the snow, its playful antics creating a joyful scene, anime watercolor painting style",
    #         "Polar bear cub resting in its mother's arms, looking cozy and safe, anime watercolor painting style",
    #         "Polar bear cub exploring an icy landscape, its curiosity evident, anime watercolor painting style",
    #         "Polar bear cub sliding down a snowy hill, looking carefree and happy, anime watercolor painting style",
    #         "Polar bear cub playing with a snowball, its playful nature shining through, anime watercolor painting style",
    #         "Polar bear cub standing on a chunk of ice, looking out at the frozen landscape, anime watercolor painting style",
    #         "Polar bear cub interacting with other cubs, creating a lively and social scene, anime watercolor painting style",
    #         "Polar bear cub lying in the snow, looking relaxed and content, anime watercolor painting style",
    #         "Polar bear cub swimming in the icy water, showcasing its resilience, anime watercolor painting style",
    #         "Polar bear cub basking in the sunlight, its fur glowing in the light, anime watercolor painting style"
    #     ],
    #     "title": "Chillhop Music",
    #     "file_name": "polar_bear_cub_music",
    #     "day_of_week": [0, 1, 2, 3, 4, 5, 6]
    # },
    {
        "short_description": [
            "Santa Claus checking his gift list in a cozy toy workshop filled with toys and tools, realistic lighting and details"
        ],
        "title": "Christmas Music",
        "file_name": "christmas_music",
        "day_of_week": [0,1,2,3,4,5,6],
    },
    # {
    #     "short_description": [
    #         "A fierce 25-year-old man in a spiked leather jacket and glowing headphones stands boldly on a chaotic festival stage with red strobe lights, smoke, embers, and roaring pyrotechnics, exuding unstoppable hardstyle energy",
    #         "A confident, slightly sexy DJ with neon-highlighted hair and sleek attire mixes tracks dynamically on a futuristic console amid vibrant lights, lasers, and smoke at an electrifying EDM festival stage",
    #     ],
    #     "title": "",
    #     "file_name": "edm_music",
    #     "day_of_week": [0,1,2,3,4,5,6],
    # }
]


DATASET_TRAINED_FOLDER = Path(os.getenv('DATASET_TRAINED_FOLDER', "/dataset_trained"))

