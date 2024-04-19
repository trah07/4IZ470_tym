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
    start_pattern = r"(?i)\b(?:about the job|responsibilities|job duties|job responsibilities)\b"
    end_pattern = r"(?i)\b(?:qualifications|requirements|what you will bring|more about this role)\b"

    start_match = re.search(start_pattern, text)
    if start_match:
        start_index = start_match.start()
    else:
        start_index = 0
    
    end_match = re.search(end_pattern, text[start_index:])
    if end_match:
        end_index = end_match.start() + start_index
    else:
        end_index = len(text)
    
    job_description = text[start_index:end_index].strip()

    sentences = sent_tokenize(job_description)
    # Token pro kapitalizaci
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    filtered_sentences = []

    for sentence in sentences:
        if any(word in sentence.lower() for word in ["qualification", "requirement", "what you will bring", "more about this role"]):
            continue

        words = word_tokenize(sentence)
        filtered_words = []
        for word, pos in pos_tag(words):
            # Token délky
            if word.lower() not in stop_words and len(word) > 3:
                word = re.sub(r'[^\w-]', '', word)
                if word:
                    if pos.startswith('V'):
                        word = stemmer.stem(word)
                    else:
                        word = lemmatizer.lemmatize(word)
                    filtered_words.append(word)
        filtered_sentence = ' '.join(filtered_words)
        if filtered_sentence:
            filtered_sentences.append(filtered_sentence)

    bullet_points = '\n• '.join(filtered_sentences)

    return bullet_points

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
    print(f"\nJob description in {file_name}:\n• {description}")
