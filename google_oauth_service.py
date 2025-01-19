#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from stable_diffusion_service import *

# from streamlit_cookies_manager import EncryptedCookieManager
from dotenv import load_dotenv;
import json;

load_dotenv()
REDIRECT_URI = 'http://127.0.0.1:5000/auth-callback'

# cookies = EncryptedCookieManager(
#     prefix = 'streamlit',
#     password = getenv("COOKIES_SECRET_KEY")
# )

# if not cookies.ready():
#     st.stop()

def create_flow():
    try:
        print("Creating flow...")
        return Flow.from_client_secrets_file(
            'ignore/client_secret.json',  # Ensure this file exists and has correct content
            scopes=[
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
            ],
            redirect_uri=REDIRECT_URI
        )
    except Exception as e:
        print("Error creating flow:", str(e))
        raise

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
    try:
        print("exchanging code for token")
        flow = create_flow()

        print("flow:", flow)

        flow.fetch_token(code=auth_code)
        print("credentials:", flow.credentials)

        return flow.credentials    

    except Exception as e:
        print("error exchanging code for token", str(e))
        raise

def fetch_user_info(token):
    try:
        print("fetching user info")
        return requests.request("GET", "https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {token}"})
    except Exception as e:
        print("error fetching user info", str(e))
        raise


# def setup_google_oauth():
    # st.title("Google Authentication")

    # if "credentials" in cookies:
        # st.write('you are already logged in')

        #unencode the credentials from json
        # credentials = json.loads(cookies['credentials'])

        #fetch the user info
        # user_info = requests.request("GET", "https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {credentials['access_token']}"})

        # if user_info.status_code == 200:
        #     #display the user info picture, and name
        #     st.image(user_info.json()['picture'])
        #     st.write(user_info.json()['name'])


    #check if the user is logged in by checking if the code is in the query params
    # if "code" in st.query_params:
        # st.write('you are currently logged in')

        # auth_code = st.query_params['code']
        # state = st.query_params['state']

        #check if the state is the same as the one in the cookies
        #this is to prevent CSRF attacks
        # if cookies['oauth_state'] != state:
        #     st.write("state is not the same as the one in the cookies")
        #     st.stop()

        #exchange the auth code for an access token
        # credentials = exchange_code_for_token(auth_code)

        #store and encode the credentials as json strings
        # cookies["credentials"] = json.dumps({
        # "access_token": credentials.token,
        # "refresh_token": credentials.refresh_token,
        # "expires_at": credentials.expiry.timestamp(),
        # })

#        cookies["user_info"] = json.dumps(user_info)  # Serialize user info as JSON
        # cookies.save()
        # st.write("credentials stored in cookies")

        #fetch the user info
        # user_info = requests.request("GET", "https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {credentials.token}"})
        # st.write("user info:")
        # st.write(user_info.json())

        #display the user info picture, and name
        # st.image(user_info.json()['picture'])
        # st.write(user_info.json()['name'])

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