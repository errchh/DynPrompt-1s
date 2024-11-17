import streamlit as st
import pandas as pd
import time

from ui_helper import render_image, file_selector

# Initialize session state for storing the DataFrame
if 'inputfile' not in st.session_state:
    st.session_state.inputfile = None


# display the logo
render_image('static/logo.png')

# display the title for the application
st.text("DynPrompt-1s: your free tool for automating repetitive tasks with generative AI",)

# display the drop
option = st.selectbox(
    "Which model you would like to use?",
    ("llama3.2:3b"),
)
st.write("You selected:", option)

# default value stored in the input box
default_value = """You are a helpful assistant expert in branding. Create a brand name using the following keyword. It must be easy to pronounce and easy to remember. 
    Provide the brand name only. 
    Keyword:\n"""

# create a box for input promt
x = st.text_input(label="Text input promt",value= default_value)

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

# Create a button for uploading the file
if st.button('Preview CSV File'):
    try:
        # Display the file uploader widget
        st.session_state.dataframe = pd.read_csv(uploaded_file)
        st.success("Here's your input!")
        # Display the DataFrame
        st.write(st.session_state.dataframe)
    except ValueError:
        st.write("File not yet selected.")
        

if st.button('Upload CSV File and Run the Script'):
   with st.spinner('Loading...'):
        time.sleep(5) # Call the long-running function

if st.button("Download output csv file"):
    st.write(st.session_state.dataframe)