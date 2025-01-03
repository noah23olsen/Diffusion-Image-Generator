import streamlit as st;

#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from stable_diffusion_service import *
from google_oauth_service import *


def main():
    setup_google_oauth()
    generate_image()
    display_images()

if __name__ == "__main__":
    main()
