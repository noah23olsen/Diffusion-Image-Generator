from stable_diffusion_service import *
from google_oauth_service import *

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap4
from os import getenv;
from datetime import datetime

app = Flask(__name__)
app.secret_key = getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

bootstrap = Bootstrap4(app)

RESOURCES_DIR = os.path.join(os.getcwd(), "resources")

# Sample blog posts data
BLOG_POSTS = {
    'future-of-ai-art': {
        'title': 'The Future of AI Art: Trends and Predictions for 2024',
        'date': 'March 15, 2024',
        'category': 'Trends',
        'image_url': '/static/example.webp',
        'description': 'Explore the latest trends in AI art generation and what the future holds for creative AI technologies.',
        'content': '''
            <h2>Introduction</h2>
            <p>As we move further into 2024, AI art generation continues to evolve at a rapid pace. This article explores the latest trends, from improved prompt engineering to the integration of AI art in professional workflows.</p>
            
            <h2>Current Trends</h2>
            <p>The AI art landscape is constantly evolving, with new techniques and applications emerging regularly. Some of the most notable trends include:</p>
            <ul>
                <li>Improved prompt engineering techniques</li>
                <li>Integration with professional creative workflows</li>
                <li>Advancements in style transfer and mixing</li>
                <li>Growing adoption in commercial applications</li>
            </ul>
            
            <h2>Looking Ahead</h2>
            <p>The future of AI art is bright, with many exciting developments on the horizon. As the technology continues to mature, we can expect to see even more innovative applications and creative possibilities.</p>
        '''
    },
    'mastering-prompts': {
        'title': 'Mastering AI Art Prompts: A Comprehensive Guide',
        'date': 'March 10, 2024',
        'category': 'Tutorial',
        'image_url': '/static/example.webp',
        'description': 'Learn the art of crafting effective prompts for AI image generation.',
        'content': '''
            <h2>Understanding Prompts</h2>
            <p>Writing effective prompts is both an art and a science. This guide covers everything from basic syntax to advanced techniques for achieving your desired artistic results.</p>
            
            <h2>Basic Prompt Structure</h2>
            <p>A well-structured prompt typically includes:</p>
            <ul>
                <li>Main subject or focus</li>
                <li>Artistic style or medium</li>
                <li>Lighting and mood</li>
                <li>Additional details and context</li>
            </ul>
            
            <h2>Advanced Techniques</h2>
            <p>For more experienced users, there are several advanced techniques that can help achieve specific results:</p>
            <ul>
                <li>Style mixing and blending</li>
                <li>Negative prompting</li>
                <li>Weighted terms</li>
                <li>Reference image integration</li>
            </ul>
        '''
    },
    'ethical-considerations': {
        'title': 'Ethical Considerations in AI Art Generation',
        'date': 'March 5, 2024',
        'category': 'Opinion',
        'image_url': '/static/example.webp',
        'description': 'Explore the ethical implications of AI-generated art and its impact on the creative industry.',
        'content': '''
            <h2>The Ethics of AI Art</h2>
            <p>As AI art generation becomes more prevalent, it's crucial to address the ethical considerations surrounding this technology. From copyright concerns to artist compensation, the intersection of AI and creativity raises important questions.</p>

            <h2>Key Ethical Considerations</h2>
            <ul>
                <li>Copyright and ownership of AI-generated art</li>
                <li>Impact on traditional artists and their livelihoods</li>
                <li>Data privacy and consent in training AI models</li>
                <li>Attribution and transparency in AI-assisted work</li>
            </ul>

            <h2>Finding Balance</h2>
            <p>The key to ethical AI art generation lies in finding a balance between innovation and respect for human creativity. This includes:</p>
            <ul>
                <li>Fair compensation models for artists</li>
                <li>Clear guidelines for AI art usage</li>
                <li>Transparency in AI-assisted creation</li>
                <li>Supporting both traditional and AI-assisted art forms</li>
            </ul>
        '''
    },
    'commercial-applications': {
        'title': 'AI Art in Commercial Applications',
        'date': 'February 28, 2024',
        'category': 'Business',
        'image_url': '/static/example.webp',
        'description': 'Discover how businesses are leveraging AI-generated art for marketing, product design, and brand development.',
        'content': '''
            <h2>Business Applications</h2>
            <p>AI art generation is revolutionizing how businesses approach visual content creation. From marketing materials to product design, the applications are vast and growing.</p>

            <h2>Key Use Cases</h2>
            <ul>
                <li>Marketing and advertising visuals</li>
                <li>Product design and prototyping</li>
                <li>Brand identity development</li>
                <li>Content creation for social media</li>
            </ul>

            <h2>Implementation Strategies</h2>
            <p>Successfully integrating AI art into business workflows requires:</p>
            <ul>
                <li>Clear brand guidelines and consistency</li>
                <li>Efficient approval processes</li>
                <li>Quality control measures</li>
                <li>Integration with existing design tools</li>
            </ul>

            <h2>ROI and Benefits</h2>
            <p>Businesses implementing AI art generation are seeing benefits in:</p>
            <ul>
                <li>Reduced production costs</li>
                <li>Faster iteration cycles</li>
                <li>Increased creative possibilities</li>
                <li>Improved time-to-market</li>
            </ul>
        '''
    },
    'science-behind-ai': {
        'title': 'The Science Behind AI Image Generation',
        'date': 'February 20, 2024',
        'category': 'Technical',
        'image_url': '/static/example.webp',
        'description': 'A deep dive into the technical aspects of how AI generates images from text prompts.',
        'content': '''
            <h2>Understanding the Technology</h2>
            <p>AI image generation is built on complex neural networks and machine learning algorithms. This article breaks down the key technical concepts in an accessible way.</p>

            <h2>Core Components</h2>
            <ul>
                <li>Neural network architectures</li>
                <li>Diffusion models</li>
                <li>Attention mechanisms</li>
                <li>Training data processing</li>
            </ul>

            <h2>The Generation Process</h2>
            <p>The process of generating an image from text involves several steps:</p>
            <ol>
                <li>Text encoding and understanding</li>
                <li>Feature extraction and mapping</li>
                <li>Image synthesis and refinement</li>
                <li>Quality enhancement and post-processing</li>
            </ol>

            <h2>Recent Advances</h2>
            <p>The field is rapidly evolving with new developments in:</p>
            <ul>
                <li>Model architecture improvements</li>
                <li>Training efficiency</li>
                <li>Output quality and consistency</li>
                <li>Resource optimization</li>
            </ul>
        '''
    }
}

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
    return render_template('blog.html', posts=BLOG_POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BLOG_POSTS.get(slug)
    if not post:
        return render_template('404.html'), 404
    return render_template('blog_post.html', post=post)

@app.route('/tutorials')
def tutorials():
    user_info = session.get('user_info')
    return render_template("tutorials.html", user_info=user_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Just show a success message without sending email
        flash('Your message has been received! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

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
