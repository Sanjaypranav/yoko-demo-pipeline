import streamlit as st
from PIL import Image
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai
from yoko.fluxapi import download_generated_image
from yoko.prompt import generate_detailed_prompt
from yoko.sdxl import from_sketch, generate_image
import tempfile

def save_uploadedfile(uploadedfile):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        img = Image.open(uploadedfile)
        img.save(tmp_file.name, format='PNG')
        return tmp_file.name

def pipeline_one(prompt_dict):
    detailed_prompt = generate_detailed_prompt(prompt_dict)
    download_generated_image(detailed_prompt)
    return Image.open("outputs/generated_image.png")

def pipeline_two(prompt_dict, sketch):
    detailed_prompt = generate_detailed_prompt(prompt_dict)
    return Image.open(from_sketch(detailed_prompt, sketch))

def pipeline_three(prompt_dict, image):
    detailed_prompt = generate_detailed_prompt(prompt_dict)
    return Image.open(generate_image(image, detailed_prompt))

st.set_page_config(page_title="yoko", layout="centered")

# Sidebar for parameter inputs
garment = st.sidebar.text_input("Garment", "Dress")
style = st.sidebar.text_input("Style", "Casual")
fabric = st.sidebar.text_input("Fabric", "Cotton")
pattern = st.sidebar.text_input("Pattern", "Solid")
neckline = st.sidebar.text_input("Neckline", "Round Neck")
sleeves = st.sidebar.text_input("Sleeves", "Short Sleeves")
hemline = st.sidebar.text_input("Hemline", "Straight")
waistline = st.sidebar.text_input("Waistline", "Relaxed")
other = st.sidebar.text_input("Other Details", "")
line_art = st.sidebar.text_input("Line Art Style", "detailed, high-resolution")

prompt_dict = {
    "Garment": garment,
    "Style": style,
    "Fabric": fabric,
    "Pattern": pattern,
    "Neckline": neckline,
    "Sleeves": sleeves,
    "Hemline": hemline,
    "Waistline": waistline,
    "Other": other,
    "Line Art": line_art
}

# Main content area
st.title("Yoko")

# Create tabs for navigation
tab1, tab2, tab3 = st.tabs(["Text-to-Image", "Sketch-to-Image", "Image-to-Image"])

with tab1:
    st.header("Text-to-Image Generation")
    if st.button("Generate Image", key="t2i_generate"):
        with st.spinner("Generating image..."):
            generated_image = pipeline_one(prompt_dict)
            st.image(generated_image, caption="Generated Image", use_column_width=True)

with tab2:
    st.header("Sketch-to-Image Generation")
    uploaded_file = st.file_uploader("Upload a sketch", type=["png", "jpg", "jpeg"], key="s2i_upload")
    if st.button("Generate Image", key="s2i_generate"):
        with st.spinner("Generating image..."):
            if uploaded_file is not None:
                sketch_path = save_uploadedfile(uploaded_file)
            else:
                sketch_path = "outputs/generated_image.png"
            generated_image = pipeline_two(prompt_dict, sketch_path)
            st.image(generated_image, caption="Generated Image", use_column_width=True)
            if uploaded_file is not None:
                os.unlink(sketch_path)

with tab3:
    st.header("Image-to-Image Generation")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"], key="i2i_upload")
    if st.button("Generate Image", key="i2i_generate"):
        with st.spinner("Generating image..."):
            if uploaded_file is not None:
                image_path = save_uploadedfile(uploaded_file)
            else:
                image_path = "outputs/castle.webp"
            generated_image = pipeline_three(prompt_dict, image_path)
            st.image(generated_image, caption="Generated Image", use_column_width=True)
            if uploaded_file is not None:
                os.unlink(image_path)
