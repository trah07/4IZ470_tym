import os
import re

def find_job_description(text):
    job_description_keywords = [
        r'\b(?:responsibilities|duties|tasks|job description)\b'
    ]

    descriptions = []

    for pattern in job_description_keywords:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        descriptions.extend(matches)

    return descriptions

folder_path = "./train/"
text_contents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text_contents.append(text)

file_names = os.listdir(folder_path)

# Nalezení náplně práce v textech
for file_name, text_content in zip(file_names, text_contents):
    file_name = os.path.splitext(file_name)[0]
    descriptions = find_job_description(text_content)
    print(f"Job descriptions in {file_name}: {descriptions}")
