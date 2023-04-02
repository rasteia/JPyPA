import requests, json, os, argparse
import frontmatter
import re

# Working image.py --all
# Command line arguments
parser = argparse.ArgumentParser(description='Generate images using the DALL-E 2 API.')
parser.add_argument('--all', action='store_true', help='Generate images for all posts.')
parser.add_argument('--select', nargs='+', help='Generate images for selected posts.')
parser.add_argument('--new', action='store_true', help='Generate images for new posts.')
args = parser.parse_args()

# API setup
with open('C:/Users/darde/code/ap.txt', 'r') as f:
    api_key = f.read().strip()
endpoint = 'https://api.openai.com/v1/images/generations'
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}',}

# Image generation
def generate_image(prompt, post_title):
    # Clean up the post title to remove invalid characters
    cleaned_title = re.sub(r'[^\w\s-]', '', post_title).strip().lower().replace(' ', '-')

    # Set up the prompt and model parameters
    data = {
        'model': 'image-alpha-001',
        'prompt': prompt,
        'num_images': 1,
        'size': '512x512',
    }

    # Make the API request
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    # Check for errors
    if response.status_code != 200:
        print(f"Error generating image: {response.json()['error']}")
        return None

    # Extract the image URL from the response
    image_url = response.json()['data'][0]['url']

    # Download the image and save it to the specified file path
    image_file = f"{cleaned_title}.png"
    image_path = os.path.join('assets', 'images', image_file)
    response = requests.get(image_url)
    with open(image_path, 'wb') as f:
        f.write(response.content)
    print(f"Generated {prompt} and saved it to '{image_path}'")

    # Return the file path of the saved image
    return image_file


# Image update in post
def update_image_in_post(post_path, image_path):
    # Load the post content from the file
    with open(post_path, 'r', encoding='utf-8') as f:
        post_content = f.read()

    # Parse the frontmatter and update the image field
    post = frontmatter.loads(post_content)
    post['image'] = image_path

    # Write the updated content back to the file
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post) + post.content)


# Process posts
if args.all:
    posts_dir = '_posts'
elif args.select:
    posts_dir = '_posts'
    selected_posts = [f"{post}.md" for post in args.select]
elif args.new:
    posts_dir = 'C:/Users/darde/Downloads/jekyllposts'
else:
    print("No posts selected. Please specify --all, --select, or --new.")
    exit()

template_path = 'C:/Users/darde/code/rasteia.github.io/templatehead.txt'
tts_script_path = 'C:/Users/darde/code/rasteia.github.io/ttsnew.py'

for file in os.listdir(posts_dir):
    if not file.endswith('.md'):
        continue
    if args.select and file not in selected_posts:
        continue
    post_path = os.path.join(posts_dir, file)
    with open(post_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    post_title = os.path.splitext(file)[0].replace('-', ' ').title()
    image_file = generate_image(f"cyberpunk {post_title}", post_title)
    if image_file is not None:
        update_image_in_post(post_path, f"/assets/images/{image_file}")
        print(f"Updated image for post: {post_title}")
    else:
        print(f"Skipping post: {post_title}. No image generated.")

def main():
    # Determine which posts to process based on command line arguments
    if args.all:
        posts_dir = '_posts'
    elif args.select:
        posts_dir = '_posts'
        selected_posts = [f"{post}.md" for post in args.select]
    elif args.new:
        posts_dir = 'C:/Users/darde/Downloads/jekyllposts'
    else:
        print("No posts selected. Please specify --all, --select, or --new.")
        return

    # Process the selected posts
    for file in os.listdir(posts_dir):
        # Skip files that are not markdown files
        if not file.endswith('.md'):
            continue

        # Skip files that are not in the selected list (if specified)
        if args.select and file not in selected_posts:
            continue

        # Extract the title of the post from the filename
        post_title = os.path.splitext(file)[0].replace('-', ' ').title()

        # Generate the image for the post
        image_file = generate_image(f"cyberpunk {post_title}", post_title)

        # If the image file was successfully generated, update the post's front matter
        if image_file is not None:
            post_path = os.path.join(posts_dir, file)
            update_image_in_post(post_path, f"/assets/images/{image_file}")
            print(f"Updated image for post: {post_title}")
        else:
            print(f"Skipping post: {post_title}. No image generated.")
if __name__ == "__main__":
    main()
