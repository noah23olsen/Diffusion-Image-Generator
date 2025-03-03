
import os;
from os import getenv;
import requests
import time
from user_service import *


API_KEY = getenv("STABILITY_API_KEY")

def store_image(response, user_input):   

    #ensure the resources directory exists
    os.makedirs(os.path.join(os.getcwd(), "resources"), exist_ok=True)

    # Replace spaces with underscores and limit to 20 characters
    user_input = user_input[:20].replace(" ", "_")

    #clean all special characters
    user_input = ''.join(e for e in user_input if e.isalnum())

    #add the timestamp to the filename
    user_input = f"{user_input}_{int(time.time())}"

    file_path = os.path.join(os.getcwd(), "resources", f"{user_input}.webp")

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path

def generate_image(prompt, output_dir="resources"):
    """Generates an AI image using Stable Diffusion 3.5 Large Turbo and saves it."""

    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {API_KEY}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, bad anatomy, distorted, deformed",
            "output_format": "png",  
            "model": "sd3.5-large-turbo",
            "steps": 35,  # The number of steps to take in the diffusion process.
            "sampler": "DPM++ 2M Karras", # the best for high-quality images while staying relatively fast.
            "mode": "text-to-image"
        },
    )

    if response.status_code == 200:
        print("Image generated successfully!")

        increment_image_count()

        return store_image(response, prompt)
    else:
        print("Error generating image:", response.json())
        raise Exception(str(response.json()))


def increment_image_count():
    """
    Increment the image count for the logged-in user.
    """
    user = get_logged_in_user()  # Fetch user object from session

    if not user:
        print("No user found.")
        return

    print(f"User found: {user.email}, current image count: {user.image_count}")

    # Use the same session to commit changes
    with Session() as session_db:
        try:
            # Attach the user object to the session
            user = session_db.merge(user)
            user.image_count += 1
            print(f"New image count: {user.image_count}")
            session_db.commit()
            print("Image count incremented successfully!")
        except Exception as e:
            session_db.rollback()
            print(f"Error updating user image count: {e}")