import os
import re
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
#spacy.load("en_core_web_sm")

# Načtení anglického jazykového modelu v SpaCy
nlp = spacy.load("en_core_web_sm")

## Gramatika pro získání názvu pracovní pozice
def get_position_title(text):
    title_indicators = ["position:", "role:", "job title:", "title:"]
    position_title = ""  
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))

    for sentence in sentences:
        sentence_lower = sentence.lower()
        for indicator in title_indicators:
            if indicator in sentence_lower:
                title = sentence.split(indicator, 1)[-1].strip()
                words = word_tokenize(title)
                filtered_words = []
                for word in words:
                    if word.lower() not in stop_words and len(filtered_words) < 4:
                        # Regex pro smazání znaků, které nejsou alfanumerické
                        word = re.sub(r'[^\w-]', '', word)
                        if word:  
                            filtered_words.append(word)
                    else:
                        break  
                position_title = ' '.join(filtered_words)
                break

    if not position_title:
        # Pokud je position_title prázdný, předpokládáme, že je to první věta
        lines = text.split('\n')
        position_title = lines[0].strip()
        words = word_tokenize(position_title)
        
        filtered_words = []
        for word in words:
            if word.lower() not in stop_words and len(filtered_words) < 4:
                word = re.sub(r'[^\w-]', '', word)
                if word:  
                    filtered_words.append(word)
            else:
                break  
        position_title = ' '.join(filtered_words)
    
    return position_title

folder_path = "./train"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

# Extrakce názvu pozice z textů
for file_name, text_content in zip(file_names, text_contents):
    file_name = os.path.splitext(file_name)[0]
    title = get_position_title(text_content)
    print(f"Position title in {file_name}: {title}")