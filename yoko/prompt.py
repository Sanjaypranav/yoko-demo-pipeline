import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_detailed_prompt(prompt_dict: dict) -> str:
    """Generates a detailed prompt for FLUX based on the input dictionary."""
    detailed_prompt = f"""
    Generate a line art image of a garment based on the following description:
    Garment: {prompt_dict.get('Garment', 'Dress')}
    Style: {prompt_dict.get('Style', 'Casual')}
    Fabric: {prompt_dict.get('Fabric', 'Cotton')}
    Pattern: {prompt_dict.get('Pattern', 'Solid')}
    Details:
    Neckline: {prompt_dict.get('Neckline', 'Round Neck')}
    Sleeves: {prompt_dict.get('Sleeves', 'Short Sleeves')}
    Hemline: {prompt_dict.get('Hemline', 'Straight')}
    Waistline: {prompt_dict.get('Waistline', 'Relaxed')}
    Other: {prompt_dict.get('Other', '')}
    Style: {prompt_dict.get('Style', 'Casual')}
    Line Art: {prompt_dict.get('Line Art', 'detailed, high-resolution')}
    NOTE: OUTPUT IMAGE GARMENT ALONE (NO BACKGROUND)
    """
    return detailed_prompt
