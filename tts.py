import os
import re
import argparse
import frontmatter
from gtts import gTTS

def clean_text(text):
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r"[\"']", "", text)  # Remove quotes and apostrophes
    text = re.sub(r'\bCopy code\b', '', text)  # Remove 'Copy code' phrase
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters except punctuation
    return text.strip()

def save_audio(text, output_file):
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save(output_file)

def write_cleaned_text_to_file(cleaned_text, file):
    with open(f"cleaned_text_{file}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(cleaned_text)

def process_posts(posts_dir, audio_dir, force=False, write_text=False):
    for file in os.listdir(posts_dir):
        if file.endswith('.md'):
            post_path = os.path.join(posts_dir, file)
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            audio_file = f"{os.path.splitext(file)[0]}.mp3"
            audio_output_path = os.path.join(audio_dir, audio_file)

            if not force and os.path.exists(audio_output_path):
                print(f"Audio file for {file} already exists. Skipping.")
                continue

            cleaned_text = clean_text(post.content)
            
            if write_text:
                write_cleaned_text_to_file(cleaned_text, file)

            save_audio(cleaned_text, audio_output_path)
            print(f"Saved audio for {file} as {audio_file}")

            post.metadata['audio_embed_code'] = f'''
            <audio controls>
              <source src="/assets/audio/{audio_file}" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>
            '''

            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))

def main():
    parser = argparse.ArgumentParser(description='Process blog posts and generate TTS audio files.')
    parser.add_argument('--force', action='store_true', help='Force processing of all posts, even if audio files already exist.')
    parser.add_argument('--t', action='store_true', help='Write cleaned text to a file for debugging and review.')

    args = parser.parse_args()

    posts_dir = './_posts'
    audio_dir = './assets/audio'
    process_posts(posts_dir, audio_dir, force=args.force, write_text=args.t)

if __name__ == "__main__":
    main()
