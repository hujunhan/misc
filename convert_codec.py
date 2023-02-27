# A script to convert a text file from one encoding to another

import os
## Convert text file from utf-16-le to utf-8
def convert_file(file_path, source_encoding, target_encoding):
    """
    Convert a text file from one encoding to another
    :param file_path: path to the text file
    :param source_encoding: source encoding
    :param target_encoding: target encoding
    :return: None
    """
    # Read the text file
    with open(file_path, 'r', encoding=source_encoding) as f:
        text = f.read()

    # Write the translated text to a file
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.txt')[0]
    file_name = file_name + '_uft8.txt'
    with open(file_name, 'w', encoding=target_encoding) as f:
        f.write(text)

import glob
file_path_list=glob.glob('/Users/hu/Downloads/test/RJ434166/eng/*.txt')
for path in file_path_list:
    convert_file(path, 'utf-16-le', 'utf-8')