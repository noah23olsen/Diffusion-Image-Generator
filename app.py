#google auth
#from google.oauth2 import id_token
#from google_auth_oauthlib.flow import Flow
#from google.auth.transport import requests

from stable_diffusion_service import *
from google_oauth_service import *

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_bootstrap import Bootstrap4



app = Flask(__name__)
bootstrap = Bootstrap4(app)

RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

#TODO: 
# 1. add google auth

@app.route('/', methods=['GET', 'POST'])
def index():
    message = request.args.get("message", "")
    image_url = request.args.get("image_url", "")
    prompt = request.args.get("prompt", "")

    if request.method == "POST":

        action = request.form["action"]

        if request.form["prompt"]:
            prompt = request.form["prompt"]
        else:
            prompt = "a random image"

        try:
            full_file_path = generate_image(prompt)

            filename = os.path.basename(full_file_path)  # Extract filename from the path (eg. image.png)
            image_url = f"/resources/{filename}"  # URL to serve the image (eg. /resources/image.png)

            return redirect(url_for("index", message=message, image_url=image_url, prompt=prompt))
        except Exception as e:
            message = f"Error generating image: {e} prompt: {prompt}"

    return render_template("index.html", message=message, image_url=image_url, prompt=prompt)

@app.route('/sign-in')
def login():
    return redirect(get_google_login_url())


# route to serve generated images (flask needs a route to serve static files)
@app.route("/resources/<path:filename>")
def resources(filename):
    """
    Serve generated images from the resources directory.
    """
    return send_from_directory(RESOURCES_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
