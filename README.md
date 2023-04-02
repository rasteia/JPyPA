# JPyPA - Jekyll Python Post Automation (JPyPA)

Jekyll Python Post Automation (JPyPA) is a set of Python scripts that work together to automate the process of creating new blog posts in Jekyll and pushing them to GitHub Pages. The system automatically processes new Markdown files placed in the `jekyllposts` folder, generating a text-to-speech audio file, updating the post's image, and pushing the changes live to your GitHub Pages site in real-time.

## Download Now

[github](https://github.com/rasteia/rasteia.github.io)

## How it works

JPyPA consists of the following Python scripts:

1.  `newpost.py`: Monitors the `jekyllposts` folder for new Markdown files, processes them, and moves them to the Jekyll `_posts` directory.
2.  `tts.py`: Converts the text content of a post to an audio file using text-to-speech.
3.  `newimage.py`: Updates the post's image based on the post's title and content.


When you save a new Markdown file in the `jekyllposts` folder, `newpost.py` detects the file and processes it in the following sequence:

1.  Copies the metadata from the `templatehead.txt` file to the new post.
2.  Updates the post title and date.
3.  Moves the processed file to the `_posts` directory and removes the original file from `jekyllposts`.
4.  Calls `tts.py` to generate an audio version of the post.
5.  Calls `newimage.py` to update the post's image.
6.  Pushes the changes to your GitHub Pages repository, making the post live.

## Usage

1.  Install the [MarkDownload] Chrome extension to easily save web content as Markdown.
2.  Configure the extension to save downloaded content to the `jekyllposts` folder.
3.  When you find interesting content on the web, use the MarkDownload extension to save it as a Markdown file in the `jekyllposts` folder.
4.  The JPyPA system will automatically process the new file and make it live on your GitHub Pages site moments later.

With JPyPA, you can quickly and easily create new blog posts from web content, complete with text-to-speech audio and relevant images, and have them go live on your site in real-time.
