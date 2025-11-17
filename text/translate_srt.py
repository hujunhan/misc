# A script to translate a text file using online api provided by Google
import requests
import json
import os
import time
import translators as ts
import translators.server as tss

src_path = r"/Users/hu/Downloads/gvh-351-faster-ja.srt"
out_path = r"/Users/hu/Downloads/gvh-351-faster-zh.srt"


def translate_file(file_path, source_language, target_language):
    """
    Translate a text file using Google Translate API
    :param file_path: path to the text file
    :param source_language: source language
    :param target_language: target language
    :return: None
    """

    # Read the text file
    with open(file_path, "r", encoding="utf-8") as f:
        ## Read file line by line and add to a list
        text = []
        original_text = []
        while True:
            line = f.readline()
            if not line:
                break
            if line == "\n" or line.strip().isdigit() or "-->" in line:
                text.append(line)
                continue
            # translated_text = tss.google(line, source_language, target_language)
            # text.append(translated_text + "\n")
            original_text.append(line.strip("\n").strip("'"))

        # text=f.read()
    print("".join(original_text))
    # print(text)
    # Translate the text
    translated_text = text
    # Get the translated text
    # translated_text = translation[0][0][0]

    # Write the translated text to a file
    with open(out_path, "w", encoding="utf-8") as f:
        # f.write(translated_text)
        for line in translated_text:
            f.write(line)

    # Wait for 1 second
    time.sleep(1)


translate_file(src_path, "ja", "zh-CN")
