import streamlit as st;

#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from stable_diffusion import *

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

def setup_google_oauth():
    st.title("Google Authentication")

    #check if the user is logged in by checking if the code is in the query params
    if "code" in st.query_params:
        st.write('you are logged in')
        st.write(st.query_params)

    #if the user clicks the button, redirect to google sign in
    if st.button("Sign in with Google"):
        auth_url = get_google_login_url()
        st.markdown(f"[Click here to sign in]({auth_url})")

        response = requests.get(auth_url)

        #TODO: implement access token refresh
        #TODO: implement access token validation
        #TODO: display user info
        
        #refer to the oauth2 documentation here: 
        # https://developers.google.com/identity/protocols/oauth2/web-server#python_2
        # https://console.cloud.google.com/apis/credentials?inv=1&invt=Abk0Ng&project=diffusion-image-generator
        


        # # example response:
        # {
        #     "state":"GHaaaaaaaaaaaaaaaaaaa"
        #     "code":"4/0AanRaaaaaaaaaaaaaaaa"
        #     "scope":"email profile openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        #     "authuser":"0"
        #     "prompt":"consent"
        # }
