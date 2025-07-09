import spacy 
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def text_summarizer(raw_docx):
    docx = nlp(raw_docx)
    stopwords = list(STOP_WORDS)
    word_frequencies = {}  
    for word in docx:  
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1

    max_freq = max(word_frequencies.values())

    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_list = list(docx.sents)
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if len(sent.text.split()) < 30:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    summarized = nlargest(7, sentence_scores, key=sentence_scores.get)
    final = ' '.join([sent.text for sent in summarized])
    return final
