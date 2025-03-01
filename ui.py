import streamlit as st
import pandas as pd
import ollama
import sys

from ui_helper import render_image

if len(sys.argv) != 2:
    sys.exit()

# Initialize session state for storing the DataFrame
if 'inputfile' not in st.session_state:
    st.session_state.inputfile = None


# display the logo
render_image('static/logo-small.png')

# display the title for the application
st.text("DynPrompt-1s: your free tool for automating repetitive tasks with generative AI",)

# display the drop
option = st.selectbox(
    "Which model you would like to use?",
    (sys.argv[1]),
)
st.write("You selected:", option)

# default value stored in the input box
default_value = """You are a helpful assistant expert in branding. Create a brand name using the following keyword. It must be easy to pronounce and easy to remember. 
    Provide the brand name only. 
    Keyword:\n"""

# create a box for input promt
x = st.text_input(label="Text input prompt",value= default_value)

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
        #def (prompt: str, file:)

        """
        # Set pwd same as app.py 
        script_dir = os.path.dirname(__file__)
        os.chdir(script_dir)
        """

        # Ollama model, error handling 
        model = option

        try:
            ollama.chat(model)
            st.write('call the LLM')
        except ollama.ResponseError as e:
            st.write('cannot call the LLM')
            if e.status_code == 404:
                ollama.pull(model)

        # Read the CSV, error handling 
    
        try:
            df = pd.read_csv(uploaded_file)
        except FileNotFoundError:
            print("The file does not exist.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except pd.errors.ParserError:
            print("Error parsing the file. Please check the file format.")

        # Column prompt_var to a list
        prompt_var_list = df.iloc[:,0].tolist()

        ##### ================================================================== #####
        #                                                                            #
        #     Edit your base prompt below                                            #
        #     Each item in data.csv will sit in a new line under the base prompt     #
        #                                                                            #
        #### =================================================================== #####

        # Base prompt
        prompt = x


        responses = []  # Create an empty list to store the responses

        # Loop variable through LLM 
        for item in prompt_var_list:
            response = ollama.chat(model=model, messages=[
                {
                    'role': 'user',
                    'content': f"""
                        {prompt}
                        {item}
                    """,
                },
            ])
            responses.append(response['message']['content'])  # Append the response to the list
            print(response['message']['content'])
            
        # Save responses list as csv
        print(responses)
        if responses:
            df_responses = pd.DataFrame(responses, columns=['responses'])  # Convert list to DataFrame
            st.session_state.dataframe = df_responses 
            st.write(st.session_state.dataframe)
            csv = df_responses.to_csv(index=False).encode('utf-8')
            st.download_button(
                label = 'Download data as CSV',
                data = csv,
                file_name = 'response.csv',
                mime ='text/csv')    
        else:
            st.write("the responses is empty")
