# A script to translate a text file using online api provided by Google
import requests
import json
import os
import time
import translators as ts
import translators.server as tss
def translate_file(file_path, source_language, target_language):
    """
    Translate a text file using Google Translate API
    :param file_path: path to the text file
    :param source_language: source language
    :param target_language: target language
    :return: None
    """
    

    # Read the text file
    with open(file_path, 'r',encoding='utf-8') as f:
        ## Read file line by line and add to a list
        text=[]
        while True:
            line=f.readline()
            if not line:
                break
            if line=='\n':
                text.append(line)
                continue
            translated_text= tss.google(line, 'en', 'zh')
            text.append(translated_text)
        # text=f.read()
        
    # print(text)
    # Translate the text
    translated_text= text
    # Get the translated text
    # translated_text = translation[0][0][0]

    # Write the translated text to a file
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.txt')[0]
    file_name = file_name + '_translated.txt'
    with open(file_name, 'w') as f:
        # f.write(translated_text)
        for line in translated_text:
            f.write(line)

    # Wait for 1 second
    time.sleep(1)
    
root_path = '/Users/hu/Downloads/test/RJ434166/eng'
import glob
file_path_list = glob.glob(root_path + '/*.txt')
print(file_path_list)
for path in file_path_list:
    translate_file(path, 'en', 'zh-CN')