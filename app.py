import streamlit as st;
import os;
import requests
from dotenv import load_dotenv;
from os import getenv;

#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

#load environment variables
load_dotenv()
api_key = getenv("STABILITY_API_KEY")

REDIRECT_URI = 'http://localhost:8501'

def get_google_login_url():
    flow = Flow.from_client_secrets_file(
        'ignore/client_secret.json',
        scopes=[
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
    )
    flow.redirect_uri = REDIRECT_URI

    #generate the google oauth login url
    authorization_url, state = flow.authorization_url(
        # enable offline access so that you can refresh an access token without re-prompting the user
        access_type="offline",
        include_granted_scopes="true",
        prompt='consent'  # forces the user to select account each time
    )
    return authorization_url

def google_auth():
    st.title("Google Authentication")

    if st.button("Sign in with Google"):
        auth_url = get_google_login_url()
        st.markdown(f"[Click here to sign in]({auth_url})")

google_auth()

#text input
user_input =  st.text_input("Enter a prompt", max_chars=50)

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

def storeImage(response):       
    with open(os.path.join(os.getcwd(), "resources", f"{user_input}.webp"), 'wb') as file:
        file.write(response.content)

#calls stable diffusions model with the prompt

def generateImage():
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {api_key}",
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
        
        storeImage(response)
    else:
        st.error("Error generating image")
        raise Exception(str(response.json()))
    

if st.button("Generate"):
    generateImage()
    


def displayImages():

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

    # Render the images in sorted order
    for file in files:
        st.image(file, caption=os.path.basename(file))


displayImages()