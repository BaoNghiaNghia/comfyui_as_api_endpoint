import os
from .celery_app import celery_app


def generate_images_api():
    """Simulate generating images by creating dummy files."""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    current_count = len(os.listdir(output_dir))
    for i in range(300 - current_count):
        file_path = os.path.join(output_dir, f"image_{current_count + i + 1}.txt")
        with open(file_path, "w") as f:
            f.write("Generated content")
    print("Images generated.")

@celery_app.task
def check_and_generate_images():
    """Check the folder and generate images if necessary."""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    item_count = len(os.listdir(output_dir))
    if item_count < 300:
        print(f"Only {item_count} items found. Generating images...")
        generate_images_api()
    else:
        print(f"Folder already has {item_count} items. No action needed.")
