from stable_diffusion_service import *
from google_oauth_service import *

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from flask_bootstrap import Bootstrap4
from os import getenv;
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap4(app)

#this is probably a bad idea to reuse the same key.. but it works haha
app.secret_key = getenv("STABILITY_API_KEY")

RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

@app.route('/', methods=['GET', 'POST'])
def index():
    message = request.args.get("message", "")
    image_url = request.args.get("image_url", "")
    prompt = request.args.get("prompt", "")
    user_info = session.get('user_info')

    if request.method == "POST":
        action = request.form.get("action", None)  # Safe way to get "action"

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

    return render_template("index.html", message=message, image_url=image_url, prompt=prompt, user_info=user_info)

@app.route('/about')
def about():
    user_info = session.get('user_info')
    return render_template("about.html", user_info=user_info)

@app.route('/blog')
def blog():
    user_info = session.get('user_info')
    return render_template("blog.html", user_info=user_info)

@app.route('/tutorials')
def tutorials():
    user_info = session.get('user_info')
    return render_template("tutorials.html", user_info=user_info)

@app.route('/contact')
def contact():
    user_info = session.get('user_info')
    return render_template("contact.html", user_info=user_info)

@app.route('/faq')
def faq():
    user_info = session.get('user_info')
    return render_template("faq.html", user_info=user_info)

@app.route('/sign-in')
def sign_in():
    return redirect(get_google_login_url())

@app.route('/auth-callback')
def auth_callback():
    auth_code = request.args.get("code")
    state = request.args.get("state")

    if auth_code and state:
        credentials = exchange_code_for_token(auth_code)
        user_info = fetch_user_info(credentials.token)

        user = store_user_info(user_info.json())

        #save user info to session so we can use it later
        session['user_info'] = user_info.json()
        return redirect(url_for("index", message="Login successful"))
    else:
        return redirect(url_for("index", message="Login failed"))
    
#logout
@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for("index", message="Logged out"))

# route to serve generated images (flask needs a route to serve static files)
@app.route("/resources/<path:filename>")
def resources(filename):
    """
    Serve generated images from the resources directory.
    """
    return send_from_directory(RESOURCES_DIR, filename)

# route to serve sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml', now=datetime.now(), request=request)

if __name__ == "__main__":
    app.run(debug=True)
