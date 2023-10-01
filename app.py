# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/error")
def error():
    return render_template("error.html")

def is_video_duration_valid(url, max_duration=120):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        duration = info_dict.get("duration", 0)
        return duration <= max_duration

def download_video(url):
    ydl_opts = {
        "format": "best",  # Change to the desired format
        "outtmpl": "downloads/%(title)s.%(ext)s",  # Output template for the downloaded file
    }

    # Download the video using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data["url"]

        # Determine if it's a YouTube URL or Instagram/Facebook URL
        if "youtube.com" in url or "youtu.be" in url:
            if is_video_duration_valid(url):
                download_video(url)
                return jsonify(message="Download successful"), 200
            else:
                return jsonify(message="Error: Video duration should not exceed 2 minutes"), 400
        else:
            if is_video_duration_valid(url):
                download_video(url)
                return jsonify(message="Download successful"), 200
            else:
                return jsonify(message="Error: Video duration should not exceed 2 minutes"), 400

    except Exception as e:
        print(str(e))
        return jsonify(message="Error: Server encountered an issue"), 500

if __name__ == "__main__":
    app.run()
