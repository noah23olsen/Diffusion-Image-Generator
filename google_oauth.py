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

def google_auth():
    st.title("Google Authentication")

    #check if the user is logged in by checking if the code is in the query params
    if "code" in st.query_params:
        st.write('you are logged in')
        st.write(st.query_params)

#        # get the access token from the code   

        if st.button("Sign in with Google"):
            auth_url = get_google_login_url()
            st.markdown(f"[Click here to sign in]({auth_url})")

    else:
        #if the user clicks the button, redirect to google sign in
        if st.button("Sign in with Google"):
            auth_url = get_google_login_url()
            st.markdown(f"[Click here to sign in]({auth_url})")

            response = requests.get(auth_url)

        # # example response:
        # {
        #     "state":"GHoPn0hkfaS2mrWYVOwvzaSDpMOozB"
        #     "code":"4/0AanRRrt_WA7R5rJbUt95XcQTaXxCtxT-RHI7zkurgHv0qQiNMBu1nEb8eOqctzfBPUWqRQ"
        #     "scope":"email profile openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        #     "authuser":"0"
        #     "prompt":"consent"
        # }
