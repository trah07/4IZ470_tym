import os
import re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

## Function to extract salary or wage information
def extract_salary(text):
    # Define regex patterns to identify salary or wage
    salary_patterns = [
        r'(?:\b(?:starting salary|salary|hourly wage|wage)\b|\b(?:€|EUR|USD|CZK)\s*\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?\b|\b\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?\s*(?:€|EUR|USD|CZK)\b)',
        r'(?:€|EUR|USD|CZK)\s*\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?'
    ]

    salary_info = []

    # Tokenize the text
    tokens = word_tokenize(text)

    # Join tokens into a single string
    text = ' '.join(tokens)

    # Search for salary patterns in the text
    for pattern in salary_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            salary_info.append(match)

    return salary_info

folder_path = "./train"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

# Extract salary information from texts
for file_name, text_content in zip(file_names, text_contents):
    file_name = os.path.splitext(file_name)[0]
    salaries = extract_salary(text_content)
    if salaries:
        print(f"Salary information in {file_name}: {', '.join(salaries)}")
    else:
        print(f"No salary information found in {file_name}")
