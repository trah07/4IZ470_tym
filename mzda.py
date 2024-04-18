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

def find_salary(text):
    salary_patterns = [
        r'(?:\b(?:starting salary|salary|hourly wage|wage)\b|\b(?:€|EUR|USD|CZK)\s*\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?\b|\b\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?\s*(?:€|EUR|USD|CZK)\b)',
        r'(?:€|EUR|USD|CZK)\s*\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?'
    ]

    salaries = []

    for pattern in salary_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        salaries.extend(matches)

    if not salaries:
        return [], [], [], [], [], []  # Return empty lists if no salaries found

    # Extract salary text
    salary_text = ' '.join(salaries)

    tokenizer = RegexpTokenizer(r'\b\w+\b')  # Tokenizer for whole words

    tokens = tokenizer.tokenize(salary_text)
    salary_tokens = [token for token in tokens if token.lower() in ['salary', 'wage']]

    # SpaCy for POS tagging and lemmatization
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(salary_text)
    sentence_tokens = [sent.text for sent in doc.sents]
    pos_tags = [(token.text, token.pos_) for token in doc]

    # NLTK for stemming
    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stems = [porter.stem(token) for token in tokens]
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    return salaries, salary_tokens, sentence_tokens, pos_tags, stems, lemmas

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
    salaries, salary_tokens, sentences, pos_tags, stems, lemmas = find_salary(text_content)
    print(f"Salaries in {file_name}: {salaries}")
    print(f"Salary tokens in {file_name}: {salary_tokens}")
    print(f"Sentences in {file_name}: {sentences}")
    print(f"POS tags in {file_name}: {pos_tags}")
    print(f"Stems in {file_name}: {stems}")
    print(f"Lemmas in {file_name}: {lemmas}")
