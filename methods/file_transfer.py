import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():

    files = request.files.getlist("file")

    image_urls = []

    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        image_urls.append(f"http://127.0.0.1:5000/uploads/{file.filename}")

    return jsonify({
        "message": "File uploaded successfully",
        "files": image_urls
    })

@app.route("/uploads/<filename>")
def show_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)