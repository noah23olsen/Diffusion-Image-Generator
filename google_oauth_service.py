from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Base, User

import requests

from os import getenv

REDIRECT_URI =  getenv("REDIRECT_URI")
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_flow():
    try:
        print("Creating flow...")
        return Flow.from_client_secrets_file(
            'client_secret.json',  # Ensure this file exists and has correct content
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

def store_user_info(user_info):
    """Store or update user information in the database."""
    session = Session()  # Create a new session
    try:
        # Extract user info from the passed JSON
        email = user_info.get('email')
        name = user_info.get('name')

        # Check if the user already exists in the database
        user = session.query(User).filter_by(email=email).first()

        if user:
            # User exists, update their information
            print("User exists, updating info...")
            user.name = name  # Update the name if it has changed
            user.updated_at = func.now()  # Automatically update the updated_at timestamp
        else:
            # Create a new user
            print("Creating new user...")
            user = User(
                name=name,
                email=email,
                image_count=0  # Default value for new users
            )
            session.add(user)  # Add the new user to the session

        # Commit the transaction to save changes
        session.commit()
        print("User info stored successfully!")
        return user  # Return the user object for further use
    except Exception as e:
        # Roll back the transaction in case of any errors
        print("Error storing user info:", str(e))
        session.rollback()
        raise
    finally:
        session.close()  # Always close the session to release resources