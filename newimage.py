import os
import sys
import openai
import subprocess
from pathlib import Path

POSTS_DIRECTORY = "_posts"
DEFAULT_IMAGE = "/assets/images/cpunk3.jfif"
API_KEY_FILE = "C:/Users/darde/code/ap.txt"

# Load API key
with open(API_KEY_FILE, "r") as file:
    api_key = file.read().strip()

openai.api_key = api_key


def update_post_image(filename, new_image_url):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()

    for index, line in enumerate(content):
        if line.startswith("image:"):
            content[index] = f"image: {new_image_url}\n"
            break

    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(content)


def generate_new_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url",
        )
        return response["data"][0]["url"]
    except Exception as e:
        print(f"Failed to generate new image: {e}")
        return DEFAULT_IMAGE


def update_posts_with_default_image():
    print("Scanning for posts with default image...")
    for post_filename in os.listdir(POSTS_DIRECTORY):
        post_file_path = os.path.join(POSTS_DIRECTORY, post_filename)

        if os.path.isfile(post_file_path):
            with open(post_file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if f"image: {DEFAULT_IMAGE}" in content:
                print(f"Found post with default image: {post_file_path}")
                prompt = Path(post_filename).stem
                new_image_url = generate_new_image(prompt)

                if new_image_url != DEFAULT_IMAGE:
                    update_post_image(post_file_path, new_image_url)
                    print(f"Updated {post_file_path} with new image: {new_image_url}")
                else:
                    print(f"Skipped {post_file_path} (unique image already set)")
            else:
                print(f"Skipped {post_file_path} (no default image found)")
        else:
            print(f"Skipped {post_file_path} (not a file)")

    print("Finished scanning for posts with default image.")


if __name__ == "__main__":
    update_posts_with_default_image()
