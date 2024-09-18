# pipeline file 

from yoko.prompt import generate_detailed_prompt
from yoko.fluxapi import download_generated_image
from rich import print as rprint
from yoko.sdxl import from_sketch
from yoko.sdxl import generate_image
# pipeline 1
# prompt to image 2D
def pipeline_one():
    user_prompt = input("Enter your prompt for the garment design: ")
    detailed_prompt = generate_detailed_prompt(user_prompt)
    download_generated_image(detailed_prompt)
    return 'Pipeline 1 completed successfully!'

# will save as generated_image.png
# pipeline 2
#sketech to image 2D
def pipeline_two():
    user_prompt = input("Enter your prompt for the garment design: ")
    from_sketch(generate_detailed_prompt(user_prompt))
    return 'Pipeline 2 completed successfully!'

# pipeline 3
# image + prompt to image 2D
def pipeline_three():
    user_prompt = input("Enter your prompt for the garment design: ")
    detailed_prompt = generate_detailed_prompt(user_prompt)
    generate_image("outputs/castle.webp", detailed_prompt)
    return 'Pipeline 3 completed successfully!'

