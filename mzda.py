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

    return salaries

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
    file_name = os.path.splitext(file_name)[0]
    salaries = find_salary(text_content)
    print(f"Salaries in {file_name}: {salaries}")
