import os
import requests
from dotenv import load_dotenv
load_dotenv()

def from_sketch(prompt: str, filename: str= "data/sketch.png")-> str:
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/control/sketch",
        headers={
            "authorization": f"Bearer {os.environ['STABILITY_API_KEY']}",
            "accept": "image/*"
        },
        files={
            "image": open(f"{filename}", "rb")
        },
        data={
            "prompt": """
            {prompt}
        NOTE: OUTPUT IMAGE GARMENT ALONE""", 
            "control_strength": 0.9,
            "output_format": "webp"
        },
    )

    if response.status_code == 200:
        with open("outputs/castle.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    return "outputs/castle.webp"


def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {os.environ['STABILITY_API_KEY']}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

def generate_image(image: str, 
                   prompt :str, 
                   negative_prompt: str = "", 
                   control_strength: float = 0.7, 
                   seed: int = 0,
                   output_format: str = "jpeg") -> str:
    """
    Function to send parameters and generate an image from the Stability AI API.
    
    Args:
        image (str): Path to the image input.
        prompt (str): The prompt to guide image generation.
        negative_prompt (str): The negative prompt to exclude certain elements.
        control_strength (float): Strength to apply control over the image.
        seed (int): Seed for random generation.
        output_format (str): Desired output format ("jpeg", "png", etc.).

    Returns:
        str: Path where the generated image is saved.
    """
    host = "https://api.stability.ai/v2beta/stable-image/control/structure"
    
    # Prepare the parameters for the request
    params = {
        "control_strength": control_strength,
        "image": image,  # Path to the image
        "seed": seed,
        "output_format": output_format,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
    }
    
    # Send request to the API
    response = send_generation_request(host, params)
    
    # Decode response content
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    response_seed = response.headers.get("seed")

    # Check for NSFW content or other issues
    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")

    # Save the generated image
    edited_image_path = "outputs/edited_image.jpg"  # Output path for the image
    with open(edited_image_path, "wb") as f:
        f.write(output_image)
    
    print(f"Image saved at {edited_image_path}")
    
    return edited_image_path