from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

REDIRECT_URI = 'http://127.0.0.1:5000/auth-callback'

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
        access_type="offline", #TODO: what does this do ?
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