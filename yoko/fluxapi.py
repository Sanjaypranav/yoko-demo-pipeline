# Description: This script demonstrates how to use the OpenAI API to generate an image based on a custom prompt.
import fal_client
import requests
from dotenv import load_dotenv
from rich import print as rprint

# Load environment variables from a .env file
load_dotenv()

def download_generated_image(prompt : str) -> str:
    # Submit the prompt to the fal_client
    handler = fal_client.submit(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt
        },
    )

    # Get the result from the handler
    result = handler.get()

    # Extract the image URL from the result
    image_url = result['images'][0]['url']

    # Download the image from the extracted URL
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the image to a file
        with open('outputs/generated_image.png', 'wb') as file:
            file.write(response.content)
        rprint('Image downloaded successfully!')
    else:
        rprint(f'Failed to download image. Status code: {response.status_code}')
    return 'outputs/generated_image.png'

# # Example usage with a custom prompt
# custom_prompt = "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture."
# download_generated_image(custom_prompt)
