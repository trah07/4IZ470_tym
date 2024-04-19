import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def get_job_description(text):
    # Accurately capture the job description section
    start_pattern = r"(?i)\bjob description\b"
    end_pattern = r"(?i)\b(?:requirements|qualifications|skills)\b"
    
    start_match = re.search(start_pattern, text)
    start_index = start_match.start() if start_match else 0
    
    end_match = re.search(end_pattern, text[start_index:])
    end_index = end_match.start() + start_index if end_match else len(text)
    
    job_description = text[start_index:end_index].strip()
    sentences = sent_tokenize(job_description)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    # Keywords and phrases to exclude that relate to benefits or perks
    exclude_keywords = [
        "benefits", "discounts", "incentive", "insurance", "pension", "scheme",
        "employee benefits", "employee discounts", "employee initiatives"
    ]

    relevant_words = []

    for sentence in sentences:
        # Exclude sentences containing benefits and perks keywords
        if any(exclude_word in sentence.lower() for exclude_word in exclude_keywords):
            continue
        
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        
        # Collect words that are not stop words and are either verbs or nouns
        for word, tag in tagged_words:
            if word.lower() not in stop_words and tag in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                if tag.startswith('V'):
                    word = stemmer.stem(word)
                else:
                    word = lemmatizer.lemmatize(word)
                relevant_words.append(word)

    return ' '.join(relevant_words)

folder_path = "./train"
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
    description = get_job_description(text_content)
    print(f"\nJob description in {file_name}: {description}")
