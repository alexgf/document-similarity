import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
from gensim.models import Phrases
import io
import requests
from PyPDF2 import PdfFileReader
from unidecode import unidecode
import re
import spacy
nlp = spacy.load('pt_core_news_sm')

def preprocess(text):
    text = re.sub(r"[^\w|\s]", "", text.lower())
    text = re.sub(r"[0-9|_]", "", text)

    stop_words = set(stopwords.words('portuguese') + 
        ['art', 'lei', 'inciso', 'capítulo', 'seção', 'resolução', 'artigo', 'nº', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix','x'] +
        ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'])

    text = " ".join([word for word in text.split() if word not in stop_words])
    
    doc = nlp(text)
    return [unidecode(token.lemma_) for token in doc if len(token.lemma_) > 2]


def trigrams(documents, min_count=5, threshold=10):
    bigram = Phrases(documents, min_count=min_count, threshold=threshold)
    trigram = Phrases(bigram[documents], min_count=min_count, threshold=threshold)

    return trigram

def text_from_pdf(url):
    r = requests.get(url)
    f = io.BytesIO(r.content)

    reader = PdfFileReader(f)
    
    content = ''
    for index in range(0, reader.numPages):
        content += reader.getPage(index).extractText().replace("\n", "")

    return content