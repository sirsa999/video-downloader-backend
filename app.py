from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])
            title = info.get("title", "No Title")

            # Choose the best downloadable format with video+audio
            best_format = next(
                (f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"),
                None
            )

            if best_format:
                video_download_url = best_format["url"]
            else:
                video_download_url = info["url"]

        return jsonify({
            "title": title,
            "video_url": video_download_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
