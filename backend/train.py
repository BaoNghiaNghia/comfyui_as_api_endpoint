import os
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionTrainer, DDPMScheduler
from transformers import AutoTokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
from .constants import DATASET_TRAINED_FOLDER

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load pre-trained model and tokenizer
model_name = "mistralai/Mistral-7B-v0.1"
pipeline = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16).to(device)
tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")

# Load and preprocess dataset
def preprocess_images(examples):
    """
    Preprocess images by resizing, normalizing, and converting them to tensors.
    
    Args:
        examples (dict): A dictionary containing paths to images under the key "image_path".
        
    Returns:
        dict: A dictionary with preprocessed image tensors under the key "pixel_values".
    """
    image_size = 512  # Target size for resizing images
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),  # Normalize to [-1, 1]
    ])
    
    preprocessed_images = []
    for path in examples["image_path"]:
        try:
            # Open and preprocess the image
            with Image.open(path).convert("RGB") as img:
                preprocessed_images.append(transform(img))
        except Exception as e:
            # Log an error message and skip the problematic image
            print(f"Error processing image {path}: {e}")
    
    return {"pixel_values": torch.stack(preprocessed_images) if preprocessed_images else torch.empty(0)}


# Replace 'custom_dataset' with the path to your dataset folder
dataset = load_dataset("imagefolder", data_dir=DATASET_TRAINED_FOLDER)
dataset = dataset.with_transform(preprocess_images)

# DataLoader
train_dataloader = DataLoader(dataset["train"], batch_size=4, shuffle=True)

# Scheduler and optimizer
noise_scheduler = DDPMScheduler.from_config(pipeline.scheduler.config)
optimizer = torch.optim.AdamW(pipeline.unet.parameters(), lr=5e-6)

# Training loop
num_epochs = 3
for epoch in range(num_epochs):
    pipeline.unet.train()
    for step, batch in enumerate(train_dataloader):
        images = batch["pixel_values"].to(device)
        noise = torch.randn_like(images).to(device)
        timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (images.shape[0],), device=device).long()

        # Add noise to the images according to the timesteps
        noisy_images = noise_scheduler.add_noise(images, noise, timesteps)

        # Get model predictions
        model_output = pipeline.unet(noisy_images, timesteps, return_dict=False)[0]

        # Compute loss
        loss = torch.nn.functional.mse_loss(model_output, noise)
        loss.backward()

        # Step optimizer and scheduler
        optimizer.step()
        optimizer.zero_grad()

        if step % 50 == 0:
            print(f"Epoch {epoch}, Step {step}, Loss: {loss.item()}")

    # Save checkpoint
    pipeline.save_pretrained(f"fine_tuned_sd_epoch_{epoch}")
    print(f"Checkpoint saved for epoch {epoch}")

print("Training complete!")
