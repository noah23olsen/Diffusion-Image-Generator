
import streamlit as st;
import os;
import requests
from dotenv import load_dotenv;
from os import getenv;

load_dotenv()
API_KEY = getenv("STABILITY_API_KEY")


#style the text input
st.markdown(
    """
    <style>
    div.stTextInput {
        background-color: #f7f7f7;
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def store_image(response, user_input):       
    with open(os.path.join(os.getcwd(), "resources", f"{user_input}.webp"), 'wb') as file:
        file.write(response.content)

#calls stable diffusions model with the prompt
def generate_image():
    #text input
    user_input =  st.text_input("Enter a prompt", max_chars=50)

    if st.button("Generate"):

        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "authorization": f"Bearer {API_KEY}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": user_input,
                "output_format": "webp",
            },
        )

        if response.status_code == 200:
            st.success("Image generated")
            
            store_image(response, user_input)
        else:
            st.error("Error generating image")
            raise Exception(str(response.json()))
    


def display_images():

    # Set the path to the resources directory
    resources_dir = os.path.join(os.getcwd(), "resources")

      # Get list of files with full paths
    files = [
        os.path.join(resources_dir, file)
        for file in os.listdir(resources_dir)
        if file.endswith(".webp")
    ]

    # Sort files by creation time (most recent first)
    files.sort(key=os.path.getctime, reverse=True)

    #render only the most recent image
    st.image(files[0], caption=os.path.basename(files[0]))

    # Render the images in sorted order
    #todo: add this back later 
    #for file in files:
     #   st.image(file, caption=os.path.basename(file))
