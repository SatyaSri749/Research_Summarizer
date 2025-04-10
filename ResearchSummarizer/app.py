from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from transformers import pipeline
import fitz  # PyMuPDF
from gtts import gTTS
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Summarizer Agent
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ----- AGENT 1: Paper Discovery Agent -----
def paper_discovery_agent(file=None, url=None, doi=None):
    pdf_path = None
    if file:
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)
    elif url:
        response = requests.get(url)
        filename = url.split("/")[-1]
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
    elif doi:
        pdf_url = resolve_doi_to_pdf(doi)
        if not pdf_url:
            return None
        response = requests.get(pdf_url)
        filename = doi.replace('/', '_') + ".pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
    return pdf_path

# ----- AGENT 2: Text Processing Agent -----
def processing_agent(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:3000]  # Limit for simplicity

# ----- AGENT 3: Summarization Agent -----
def summarization_agent(text):
    chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
    summary = ""
    for chunk in chunks[:3]:
        result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + " "
    return summary

# ----- AGENT 4: Topic Classification Agent -----
def topic_classifier_agent(text):
    topics = {
        "Artificial Intelligence": ["AI", "machine learning", "neural", "deep learning"],
        "Healthcare": ["medicine", "health", "clinical", "hospital"],
        "Education": ["learning", "education", "students", "teaching"],
    }
    for topic, keywords in topics.items():
        if any(word.lower() in text.lower() for word in keywords):
            return topic
    return "General"

# ----- AGENT 5: Audio Generation Agent -----
def audio_agent(text, filepath):
    tts = gTTS(text)
    audio_filename = os.path.splitext(os.path.basename(filepath))[0] + '.mp3'
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    tts.save(audio_path)
    return '/' + audio_path

# DOI Resolver Utility
def resolve_doi_to_pdf(doi):
    try:
        headers = {"Accept": "application/json"}
        r = requests.get(f"https://api.unpaywall.org/v2/{doi}?email=your@email.com", headers=headers)
        data = r.json()
        return data.get('best_oa_location', {}).get('url_for_pdf')
    except:
        return None

# Favicon route to prevent 500 error
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    url = request.form.get('url')
    doi = request.form.get('doi')

    pdf_path = paper_discovery_agent(file, url, doi)
    if not pdf_path:
        return "Failed to retrieve or upload the document."

    text = processing_agent(pdf_path)
    summary = summarization_agent(text)
    topic = topic_classifier_agent(summary)
    audio_path = audio_agent(summary, pdf_path)
    citation = url or doi or "Local Upload"

    return render_template('result.html', summary=summary, audio_path=audio_path, topic=topic, citation=citation)

@app.route('/<path:path>')
def send_uploaded_file(path):
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
