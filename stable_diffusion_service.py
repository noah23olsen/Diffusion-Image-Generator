
import os;
import requests
from dotenv import load_dotenv;
from os import getenv;

# load_dotenv()
API_KEY = getenv("STABILITY_API_KEY")

def store_image(response, user_input):       
    #ensure the resources directory exists
    os.makedirs(os.path.join(os.getcwd(), "resources"), exist_ok=True)

    # Replace spaces with underscores and limit to 20 characters
    user_input = user_input[:20].replace(" ", "_")
    
    #clean all special characters
    user_input = ''.join(e for e in user_input if e.isalnum())

    file_path = os.path.join(os.getcwd(), "resources", f"{user_input}.webp")

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path

# #calls stable diffusions model with the prompt
def generate_image(prompt, output_dir="resources"):
    
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {API_KEY}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "webp",
        },
    )

    if response.status_code == 200:
        print("Image generated")
        
        return store_image(response, prompt)
    else:
        print("Error generating image")
        raise Exception(str(response.json()))
    


# def display_images():

#     # Set the path to the resources directory
#     resources_dir = os.path.join(os.getcwd(), "resources")

#       # Get list of files with full paths
#     files = [
#         os.path.join(resources_dir, file)
#         for file in os.listdir(resources_dir)
#         if file.endswith(".webp")
#     ]

#     # Sort files by creation time (most recent first)
#     files.sort(key=os.path.getctime, reverse=True)

#     #render only the most recent image
#     st.image(files[0], caption=os.path.basename(files[0]))

#     # Render the images in sorted order
#     #todo: add this back later 
#     #for file in files:
#      #   st.image(file, caption=os.path.basename(file))
