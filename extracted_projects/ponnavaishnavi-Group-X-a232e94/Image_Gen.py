# ✅ Install required packages
!pip install -q diffusers transformers accelerate torch pillow
print("✅ Packages installed!")

# ✅ Import libraries
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
from IPython.display import display

print("GPU Available:", torch.cuda.is_available())
print("✅ Libraries imported!")

# ⏳ Load Stable Diffusion model
print("⏳ Loading AI model... (this takes 3–5 minutes on first run)")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    safety_checker=None
).to("cuda")
print("✅ Model loaded! Ready to generate images!")

# 🎨 Generate image from text
prompt = "photosynthesis process to understand"
print(f"🎨 Generating image for prompt: '{prompt}'")

image = pipe(prompt, num_inference_steps=30).images[0]

# 💾 Display and save image
display(image)
image.save("generated_image.png")

print("✅ Done! Image saved as generated_image.png")
