from flask import Flask, request, render_template, send_file
import pdfplumber, requests, os

app = Flask(__name__)
VOICERSS_KEY = os.getenv("VOICERSS_KEY")

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text.strip()

def text_to_speech(text, lang="ar-eg"):
    url = "https://api.voicerss.org/"
    params = {
        "key": VOICERSS_KEY,
        "hl": lang,
        "src": text[:10000],  # VoiceRSS limit
        "c": "mp3",
        "f": "44khz_16bit_stereo"
    }
    r = requests.get(url, params=params)
    with open("output.mp3", "wb") as f:
        f.write(r.content)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf"]
        lang = request.form.get("voice", "ar-eg")
        file.save("uploaded.pdf")
        text = extract_text("uploaded.pdf")
        text_to_speech(text, lang)
        return send_file("output.mp3", as_attachment=True)
    return render_template("index.html")
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
