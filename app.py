from flask import Flask, render_template, request
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import logging

app = Flask(__name__)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html', tab='home')

@app.route('/summarize', methods=['POST'])
def summarize():
    raw_text = request.form.get('rawtext', '').strip()
    algo = request.form.get('algo', '')

    if not raw_text:
        return render_template('index.html', error="Please enter some text to summarize.", tab='home')

    if algo == 'spacy':
        summary = text_summarizer(raw_text)
    elif algo == 'nltk':
        summary = nltk_summarizer(raw_text)
    else:
        summary = "Invalid method."

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', summary=summary, original_text=raw_text, algo=algo, time=time, tab='home')

@app.route('/url_summary', methods=['POST'])
def url_summary():
    url = request.form.get('url', '')
    algo = request.form.get('algo', '')
    try:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        fetched_text = ' '.join(p.text for p in soup.find_all('p'))

        if algo == 'spacy':
            summary = text_summarizer(fetched_text)
        elif algo == 'nltk':
            summary = nltk_summarizer(fetched_text)
        else:
            summary = "Invalid method."

        return render_template('index.html', summary=summary, original_text=fetched_text, url=url, algo=algo, tab='url')
    except Exception as e:
        logging.error(f"Error fetching URL: {e}")
        return render_template('index.html', error="URL couldn't be processed.", url=url, tab='url')

@app.route('/file_summary', methods=['POST'])
def file_summary():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part.", tab='file')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file.", tab='file')
    
    try:
        text = file.read().decode('utf-8')
        algo = request.form.get('algo', '')
        if algo == 'spacy':
            summary = text_summarizer(text)
        elif algo == 'nltk':
            summary = nltk_summarizer(text)
        else:
            summary = "Invalid method."

        return render_template('index.html', summary=summary, original_text=text, algo=algo, tab='file')
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return render_template('index.html', error="Error processing file.", tab='file')

@app.route('/compare', methods=['POST'])
def compare():
    try:
        text = request.form.get('compare_text', '').strip()
        if not text:
            return render_template('index.html', error="Please enter text to compare.", tab='compare')

        logging.debug(f"Compare text received: {text[:100]}...")

        spacy_summary = text_summarizer(text)
        nltk_summary = nltk_summarizer(text)

        return render_template('index.html',
                               compare_spacy=spacy_summary,
                               compare_nltk=nltk_summary,
                               compare_text=text,
                               tab='compare')
    except Exception as e:
        logging.error(f"Compare route error: {e}")
        return render_template('index.html', error="An unexpected error occurred while comparing.", tab='compare')

if __name__ == '__main__':
    app.run(debug=True)
