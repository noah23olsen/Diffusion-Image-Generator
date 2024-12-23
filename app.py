import streamlit as st;

#google auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

from stable_diffusion import *
from google_oauth import *


def main():

    google_auth()


    generate_image()


    display_images()

if __name__ == "__main__":
    main()
