import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

## Function to extract type of employment contract
def extract_employment_contract(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)

    # Initialize stemmer and lemmatizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    # Define employment contract keywords
    contract_keywords = {"full-time", "part-time", "contract", "permanent", "temporary", "freelance"}

    # Initialize contract types set
    contract_types = set()

    # Process each sentence
    for sentence in sentences:
        # Tokenize sentence into words
        words = word_tokenize(sentence)

        # Perform POS tagging
        tagged_words = pos_tag(words)

        # Extract lemmatized and stemmed forms of words
        lemmas = [lemmatizer.lemmatize(word.lower()) for word, _ in tagged_words]
        stems = [stemmer.stem(word.lower()) for word, _ in tagged_words]

        # Combine lemmatized and stemmed forms
        word_forms = lemmas + stems

        # Check for contract keywords
        for word in word_forms:
            if word in contract_keywords:
                contract_types.add(word)

    if contract_types:
        return ", ".join(contract_types)
    else:
        return "No specific contract mentioned"

folder_path = "./train"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

# Extract employment contract information from texts
for file_name, text_content in zip(file_names, text_contents):
    file_name = os.path.splitext(file_name)[0]
    employment_contract = extract_employment_contract(text_content)
    print(f"\nEmployment contract information in {file_name}:\n• {employment_contract}")
