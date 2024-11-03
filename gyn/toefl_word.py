import requests
from bs4 import BeautifulSoup
import docx
import time
import eng_to_ipa as p
import pickle
import os

import re
from docx import Document

doc_path = r"/Users/hu/Downloads/1_3.托福TOEFL学科词汇.docx"
output_path = r"/Users/hu/Downloads/1_3.托福TOEFL学科词汇_with_phonetics.md"


def extract_english_chinese_pairs(docx_path):
    # Load the document
    doc = Document(docx_path)

    # Combine all paragraphs into one text
    text = "\n".join([para.text for para in doc.paragraphs])

    # Regex to match English words followed by Chinese translations
    pattern = r"([a-zA-Z()\s]+)\s+([\u4e00-\u9fff\s]+)"
    matches = re.findall(pattern, text)

    # Create dictionary of English words and their corresponding Chinese translations
    translations = {english.strip(): chinese.strip() for english, chinese in matches}

    return translations


def get_us_phonetic(word):
    # Use an API to get the US phonetic symbol for the word
    return p.convert(word)


def extract_english_chinese_pairs_with_phonetics(docx_path):
    translations = extract_english_chinese_pairs(docx_path)
    temp_file = "./gyn/symbol.pkl"
    # check if the file exists
    if os.path.exists(temp_file):
        with open(temp_file, "rb") as f:
            return pickle.load(f)

    # Add US phonetic symbols to each English word
    translations_with_phonetics = {}
    count = 0
    for english, chinese in translations.items():
        phonetic = get_us_phonetic(english)
        translations_with_phonetics[english] = {
            "chinese": chinese,
            "phonetic": phonetic,
        }
    pickle.dump(translations_with_phonetics, open(temp_file, "wb"))
    return translations_with_phonetics


def generate_markdown_file(docx_path, output_path):
    # Extract translations with phonetics
    translations = extract_english_chinese_pairs_with_phonetics(docx_path)

    # Create markdown content
    markdown_content = "| English | Chinese | Phonetic Symbol |\n"
    markdown_content += "|---------|---------|----------------|\n"
    for english, data in translations.items():
        chinese = data["chinese"]
        phonetic = data["phonetic"] if data["phonetic"] else "N/A"
        markdown_content += f"| {english} | {chinese} | {phonetic} |\n"

    # Write to markdown file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)


# Example usage
generate_markdown_file(doc_path, output_path)
