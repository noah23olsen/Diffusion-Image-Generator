#import streamlit as st;

#google auth
#from google.oauth2 import id_token
#from google_auth_oauthlib.flow import Flow
#from google.auth.transport import requests

from stable_diffusion_service import *
#from google_oauth_service import *

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == "POST":
        prompt = request.form.get("prompt") # prompt comes from the HTML form
        try:
            file_path = generate_image(prompt)
            message = f"Image generated successfully! Saved at: {file_path}"
        except Exception as e:
            message = f"Error generating image: {e}"

    return render_template("index.html", message=message)


#def main():
    #setup_google_oauth()
    #generate_image()
    #display_images()

if __name__ == "__main__":
    #main()
    app.run(debug=True)
