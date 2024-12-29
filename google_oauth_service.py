import streamlit as st;

#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from stable_diffusion_service import *

REDIRECT_URI = 'http://localhost:8501'


def create_flow():
     return Flow.from_client_secrets_file(
        'ignore/client_secret.json',
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
        redirect_uri=REDIRECT_URI
    )

def get_google_login_url():

    flow = create_flow()

    #generate the google oauth login url
    authorization_url, state = flow.authorization_url(
        # enable offline access so that you can refresh an access token without re-prompting the user
        access_type="offline",  
        include_granted_scopes="true",
        prompt='consent'  # forces the user to select account each time
    )

    return authorization_url

def exchange_code_for_token(auth_code):
    #exchange the auth code for an access token
    flow = create_flow()

    response = flow.fetch_token(code=auth_code)
    st.write("exchange code response")
    st.write(response)
    print(response)

    return flow.credentials    


def setup_google_oauth():
    st.title("Google Authentication")

    #check if the user is logged in by checking if the code is in the query params
    if "code" in st.query_params:
        st.write('you are logged in')
        st.write(st.query_params)

        auth_code = st.query_params['code']
        st.write("auth code:" + auth_code)

        state = st.query_params['state']
        st.write("state:" + state)
        st.write("fetching auth token")

        #exchange the auth code for an access token
        credentials = exchange_code_for_token(auth_code)

        #store the credentials in session state
        st.session_state['credentials'] = credentials
        st.write("credentials stored in session state")

        #fetch the user info
        user_info = requests.request("GET", "https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {credentials.token}"})
        st.write("user info:")
        st.write(user_info.json())

        #display the user info picture, and name
        st.image(user_info.json()['picture'])
        st.write(user_info.json()['name'])


        

    #if the user clicks the button, redirect to google sign in
    if st.button("Sign in with Google"):
        auth_url = get_google_login_url()
        st.markdown(f"[Click here to sign in]({auth_url})")


        #TODO: implement access token refresh
        #TODO: implement access token validation
        #TODO: display user info
        
        #refer to the oauth2 documentation here: 
        # https://developers.google.com/identity/protocols/oauth2/web-server#python_2
        # https://console.cloud.google.com/apis/credentials?inv=1&invt=Abk0Ng&project=diffusion-image-generator
        #print the state:        


        # # example response:
        # {
        #     "state":"GHaaaaaaaaaaaaaaaaaaa"
        #     "code":"4/0AanRaaaaaaaaaaaaaaaa"
        #     "scope":"email profile openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        #     "authuser":"0"
        #     "prompt":"consent"
        # }