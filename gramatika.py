import requests
from bs4 import BeautifulSoup
import spacy
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Načtení anglického jazykového modelu v SpaCy
nlp = spacy.load("en_core_web_sm")

# Inicializace lemmatizeru a stemmeru pro NLTK
lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()

# Seznam pro uložení lemmatizovaných a stemovaných slov
lemmatized_words = []
stemmed_words = []

# Seznam pro uložení tokenů s jejich charakteristikami
token_characteristics = []

# Načtení dat z jednotlivých odkazů
urls = [
    "https://www.linkedin.com/jobs/view/3807148745/?referenceId=kmXjhYQTy1AkVho1xvY8cw%3D%3D&eBP=CwEAAAGOfA_AkAMbUpFvmxQfKWA5pD1w54SKx6EwW748AKXs86nvE6Kn6XynnzEIh7nLOJA56Rd67YT3lWeMAiBIarLP7whZGDtOQQ2pRlYGK-07YAj_8pH1_vgthsy4wg6E3tzWlcHmwKQZ19xmlMdoxcqpWmN0ifrwHTmdUjSqjQy8io6F2FSleW02-4QDmLKi3ruVPOw1VUOaAVmFN5ERXNPJg3IWhHtIoC81Cpnd3yoAvkm2vu7KGdWmxBda8dOKfi8vKS5N225LSN---yU2Jy0QV8KOeZJlsrXdflu9xRRtlHbMKfJ7pAh_QXQHjGgDgLhuIdxLhZAK65yFcR_xnjB-GqF1Q4k_ocIxittaS_WpSzjkVkr3uw",
    "https://europa.eu/eures/portal/jv-se/jv-details/MjMyOTQ0MCAxOA?lang=en",
    "https://www.jobs.com/en-us/jobs/search?q=business+developer&where=&so=m.u.sh"
]

# Načtení a zpracování dat z jednotlivých odkazů
for url in urls:
    # Stahování obsahu webové stránky
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Získání textu z webové stránky
    text = soup.get_text()
    
    # Tokenizace vět
    sentences = sent_tokenize(text)
    
    # Procházení vět
    for sentence in sentences:
        # Tokenizace slov pomocí SpaCy
        doc = nlp(sentence)
        
        # Procházení tokenů
        for token in doc:
            # Charakteristiky tokenu
            token_characteristics.append({
                "text": token.text,
                "typ": type(token),
                "kapitalizace": (token.is_upper, token.is_lower, token.is_title),
                "délka": len(token.text),
                "doslovné_řetězce": token.text,
                "POS_značka": token.pos_,
                "stem": porter_stemmer.stem(token.text),
                "lemmatum": lemmatizer.lemmatize(token.text)
            })

# Výpis charakteristik tokenů
for token_info in token_characteristics:
    print("Token:", token_info["text"])
    print("\tTyp:", token_info["typ"])
    print("\tKapitalizace:", token_info["kapitalizace"])
    print("\tDélka:", token_info["délka"])
    print("\tDoslovné řetězce:", token_info["doslovné_řetězce"])
    print("\tPOS značka:", token_info["POS_značka"])
    print("\tStem:", token_info["stem"])
    print("\tLemmatum:", token_info["lemmatum"])
    print()
