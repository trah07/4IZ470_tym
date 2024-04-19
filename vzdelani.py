import nltk
from nltk.chunk import RegexpParser
from nltk.tokenize import word_tokenize

def extract_education_level(text):
    grammar = r"""
        EDUCATION: {<JJ|NN.*><POS>*<NN.*>}
        """
    
    chunk_parser = RegexpParser(grammar)
    
    tokens = word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)
    
    chunked_tokens = chunk_parser.parse(tagged_tokens)
    
    education_levels = set()
    for subtree in chunked_tokens.subtrees():
        if subtree.label() == 'EDUCATION':
            education_level = ' '.join(token[0] for token in subtree.leaves())
            if 'degree' in education_level.lower() or 'diploma' in education_level.lower():
                education_levels.add(education_level)
    
    if education_levels:
        return list(education_levels)
    else:
        return "Education requirement not mentioned"

folder_path = "inzeraty/train"
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
    education_requirement = extract_education_level(text_content)
    print(f"\nHighest education requirement in {file_name}:\n• {education_requirement}")
