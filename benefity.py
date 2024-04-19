import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def load_gazetteer(file_path):
    gazetteer = set()
    with open(file_path, 'r') as file:
        for line in file:
            item = line.strip().lower()
            if item:
                gazetteer.add(item)
    return gazetteer

gazetteer = load_gazetteer('gazetteer/benefits_gazetteer.txt')

def extract_benefits(text, gazetteer):
    benefits = []
    sentences = sent_tokenize(text)
    context_words = ["benefits", "package", "access", "eligible", "entitlement", "include", "offer", "provide", "scheme", "incentive", "insurance"]
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
        matched_tokens = set(token for token in tokens if token in gazetteer)
        if matched_tokens and any(context_word in sentence.lower() for context_word in context_words):
            benefits.append(sentence)
    return benefits

folder_path = "./train"
extracted_benefits = {}

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            benefits = extract_benefits(text, gazetteer)
            extracted_benefits[filename] = benefits

for file_name, benefits in extracted_benefits.items():
    file_name = os.path.splitext(file_name)[0]
    if benefits:
        print(f"Benefits in {file_name}:")
        for benefit in benefits:
            print(benefit)
    else:
        print(f"No job benefits found in {file_name}.")
    print("\n")
