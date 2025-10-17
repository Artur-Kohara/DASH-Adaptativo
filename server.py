"""
===============================
Servidor DASH Simples com Flask
===============================

 Requisitos:
- Python 3.7+
- Flask instalado:
    pip install flask

 Estrutura de pastas:
    segments/
        ├── 360p/segment.mp4
        ├── 480p/segment.mp4
        ├── 720p/segment.mp4
        └── 1080p/segment.mp4

Criação rápida das pastas e arquivos simulados (Linux/macOS):

    mkdir -p segments/360p segments/480p segments/720p segments/1080p
    echo "dummy data" > segments/360p/segment.mp4
    cp segments/360p/segment.mp4 segments/480p/segment.mp4
    cp segments/360p/segment.mp4 segments/720p/segment.mp4
    cp segments/360p/segment.mp4 segments/1080p/segment.mp4

Execução do servidor:

    python server.py

Acesse o manifesto em:
    http://127.0.0.1:5000/manifest.mpd
"""



from flask import Flask, jsonify, send_file, request
import time

app = Flask(__name__)
def log_request_info():
    print("REQUEST:")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Headers: {request.headers}")

@app.route("/manifest.mpd")
def manifest():
    return jsonify({
        "video": {
            "representations": [
                {"id": "360p", "bandwidth": 500, "url": "http://localhost:5000/video/360p"},
                {"id": "480p", "bandwidth": 1000, "url": "http://localhost:5000/video/480p"},
                {"id": "720p", "bandwidth": 2500, "url": "http://localhost:5000/video/720p"},
                {"id": "1080p", "bandwidth": 5000, "url": "http://localhost:5000/video/1080p"},
            ]
        }
    })

@app.route("/video/<quality>")
def video_segment(quality):
    # Simulate file size by delaying response
    file_map = {
        "360p": ("segments/360p/segment.mp4", 0.5),
        "480p": ("segments/480p/segment.mp4", 0.8),
        "720p": ("segments/720p/segment.mp4", 1.2),
        "1080p": ("segments/1080p/segment.mp4", 1.8),
    }
    file, delay = file_map.get(quality, ("segments/360p_segment.mp4", 0.5))
    time.sleep(delay)  # Simulate download time based on quality
    return send_file(file, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
