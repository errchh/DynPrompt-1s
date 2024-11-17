import streamlit as st
import base64
import os

def render_image(filepath: str):
   """
   filepath: path to the image. Must have a valid file extension.
   """
   mime_type = filepath.split('.')[-1:][0].lower()
   with open(filepath, "rb") as f:
    content_bytes = f.read()
    content_b64encoded = base64.b64encode(content_bytes).decode()
    image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
    st.image(image_string)


def file_selector(folder_path='.'):
    # List all files in the specified folder
    filenames = os.listdir(folder_path)
    # Create a selectbox for file selection
    selected_filename = st.selectbox('Select a file', filenames)
    # Return the full path of the selected file
    return os.path.join(folder_path, selected_filename)