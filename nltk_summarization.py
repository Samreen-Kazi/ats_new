import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

def nltk_summarizer(raw_text):
    stopWords = set(stopwords.words("english"))
    word_frequencies = {}
    for word in nltk.word_tokenize(raw_text):
        if word.lower() not in stopWords and word.isalnum():
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    max_freq = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_list = sent_tokenize(raw_text)
    sentence_scores = {}
    for sent in sentence_list:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies and len(sent.split(' ')) < 30:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)
