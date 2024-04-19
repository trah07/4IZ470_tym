import os
import re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

## Function to extract highest education requirement
def extract_education_requirement(text):
    # Define patterns to identify education-related sections
    education_patterns = [
        r"(?i)\b(?:education|educational qualifications|educational requirement|required education)\b",
        r"(?i)\b(?:master(?:'s)? degree|master(?:'s)? equivalent|bachelor(?:'s)? degree|phd|doctorate|mba|master of business administration|bs|ba)\b"
    ]

    # Find start and end of education-related sections
    start_index = None
    end_index = None

    for pattern in education_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            if start_index is None or match.start() < start_index:
                start_index = match.start()
            if end_index is None or match.end() > end_index:
                end_index = match.end()

    if start_index is not None and end_index is not None:
        education_text = text[start_index:end_index]
    else:
        return "Education requirement not found."

    # Tokenize the education section
    tokens = word_tokenize(education_text)

    # Find the highest degree mentioned in the education section
    bachelor_degree = re.search(r"(?i)\b(?:bachelor(?:'s)? degree|bs|ba)\b", education_text)
    master_degree = re.search(r"(?i)\b(?:master(?:'s)? degree|phd|doctorate|mba|master of business administration)\b", education_text)

    if master_degree and bachelor_degree:
        if master_degree.start() > bachelor_degree.start():
            highest_degree = "Master's degree"
        else:
            highest_degree = "Bachelor's degree"
    elif master_degree:
        highest_degree = "Master's degree"
    elif bachelor_degree:
        highest_degree = "Bachelor's degree"
    else:
        highest_degree = "No specific degree mentioned"

    return highest_degree

folder_path = "./test"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

# Extract education requirement from texts
for file_name, text_content in zip(file_names, text_contents):
    file_name = os.path.splitext(file_name)[0]
    education_requirement = extract_education_requirement(text_content)
    print(f"\nHighest education requirement in {file_name}:\n• {education_requirement}")
