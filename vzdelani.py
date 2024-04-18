import requests
import os
import re
from bs4 import BeautifulSoup
import spacy
import glob
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def find_education_requirement(text):
    education_patterns = [
        r'\b(?:education|qualification|degree)\b(.+?)(?=\b(?:role|job\s*description|responsibilities|duties|$))'
    ]

    education_requirements = []

    for pattern in education_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        education_requirements.extend(matches)

    if not education_requirements:
        return [], [], [], [], [], []  # Return empty lists if no education requirements found

    # Extract education requirement text from matches
    education_requirement_text = ' '.join(education_requirements)

    tokenizer = RegexpTokenizer(r'\b\w+\b')  # Tokenizer for whole words

    tokens = tokenizer.tokenize(education_requirement_text)
    education_tokens = [token for token in tokens if token.lower() in ['education', 'qualification', 'degree']]

    # SpaCy for POS tagging and lemmatization
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(education_requirement_text)
    sentence_tokens = [sent.text for sent in doc.sents]
    pos_tags = [(token.text, token.pos_) for token in doc]

    # NLTK for stemming and lemmatization
    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stems = [porter.stem(token) for token in tokens]
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    return education_requirements, education_tokens, sentence_tokens, pos_tags, stems, lemmas

folder_path = "./train/"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

for file_name, text_content in zip(file_names, text_contents):
    print("\n")
    file_name = os.path.splitext(file_name)[0]
    education_reqs, education_tokens, sentences, pos_tags, stems, lemmas = find_education_requirement(text_content)
    print(f"Educational requirements regex in {file_name}: {education_reqs}")
    print(f"Educational requirement tokens in {file_name}: {education_tokens}")
    # print(f"Sentences in {file_name}: {sentences}")
    # print(f"POS tags in {file_name}: {pos_tags}")
    # print(f"Stems in {file_name}: {stems}")
    # print(f"Lemmas in {file_name}: {lemmas}")
