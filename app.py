#google auth
#from google.oauth2 import id_token
#from google_auth_oauthlib.flow import Flow
#from google.auth.transport import requests

from stable_diffusion_service import *
#from google_oauth_service import *

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    image_url = ""

    if request.method == "POST":
        prompt = request.form.get("prompt") # prompt comes from the HTML form
        try:
            full_file_path = generate_image(prompt)
            message = f"Image generated successfully! Saved at: {full_file_path}"

            filename = os.path.basename(full_file_path)  # Extract filename from the path (eg. image.png)
            image_url = f"/resources/{filename}"  # URL to serve the image (eg. /resources/image.png)
        except Exception as e:
            message = f"Error generating image: {e}"

    return render_template("index.html", message=message, image_url=image_url)


# route to serve generated images (flask needs a route to serve static files)
@app.route("/resources/<path:filename>")
def resources(filename):
    """
    Serve generated images from the resources directory.
    """
    return send_from_directory(RESOURCES_DIR, filename)

#def main():
    #setup_google_oauth()
    #generate_image()
    #display_images()

if __name__ == "__main__":
    #main()
    app.run(debug=True)
