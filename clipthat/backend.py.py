import os
from flask import Flask, request, send_file, render_template, jsonify
import yt_dlp  # Ensure yt_dlp is installed and imported

# Define paths for templates and downloads folders
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Ensure the downloads folder exists
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    format_type = request.form.get('format', 'video')  # Default to 'video'
    quality = request.form.get('quality', 'best')     # Default to 'best'

    # Map quality to yt-dlp formats
    if quality == "best":
        format_string = "bestvideo+bestaudio"
    elif quality == "720p":
        format_string = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "480p":
        format_string = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    elif quality == "360p":
        format_string = "bestvideo[height<=360]+bestaudio/best[height<=360]"
    elif quality == "audio_only":
        format_string = "bestaudio"
    else:
        format_string = "bestvideo+bestaudio"  # Fallback to best quality

    # yt-dlp options
    options = {
        'format': format_string,
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
        'merge_output_format': 'mp4',  # Ensure faster merging
        'n_threads': 4,  # Use threading for faster downloads
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/clear', methods=['POST'])
def clear_downloads():
    # Optional: Clear the downloads folder
    for file in os.listdir(DOWNLOADS_DIR):
        os.remove(os.path.join(DOWNLOADS_DIR, file))
    return jsonify({'message': 'Downloads cleared!'})

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # Handle the form data (e.g., save it, send an email, etc.)
    return jsonify({"status": "success", "message": "Thank you for contacting us!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
