from spellchecker import SpellChecker
import re
import glob
import nltk
import pickle
import os

nltk.download("punkt")
# define the origin folder
pre_path = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes"
os.chdir(pre_path)
md_path = sorted(glob.glob("**/*.md", recursive=True))

output_path = "/Users/hu/Downloads/test"

exclude_words = [
    "ml",
    "bayes",
    "mathjax",
    "argmax",
    "indep",
    "https",
    "predefined",
    "dataset",
    "estimator",
    "approximator",
]

# store the choice of the user
if glob.glob("data/choice.pkl"):
    with open("data/choice.pkl", "rb") as f:
        choice = pickle.load(f)
else:
    choice = {}

# store checked files
if glob.glob("data/checked_files.pkl"):
    with open("data/checked_files.pkl", "rb") as f:
        checked_files = pickle.load(f)
else:
    checked_files = []


def extract_words(text):
    words = nltk.word_tokenize(text)
    # filter out punctuation
    words = [word for word in words if word.isalpha() and len(word) > 1]
    # filter out words contain Chinese characters
    words = [word for word in words if not re.search("[\u4e00-\u9fff]", word)]
    return words


def check_spelling(word, spellchecker):
    """Check if the given word is spelled correctly."""
    return word not in spellchecker.unknown([word])


def annotate_mistakes(text, spellchecker):
    """Annotate misspelled words in the given text."""
    words = extract_words(text)
    # print(words)

    for word in words:
        if word in exclude_words:
            continue
        if not check_spelling(word, spellchecker):
            # Print context with annotated wrong word
            # start = max(text.find(word) - 30, 0)
            # end = min(text.find(word) + len(word) + 30, len(text))
            # annotated_word = "||" + word + "||"
            # context = text[start:end].replace(word, annotated_word)
            # print(context)
            # print("----------------------------")  # Separator
            # Print the word with its suggested corrections
            print(f"{word}: {spellchecker.correction(word)}")
            if word in choice:
                a = choice[word]
            else:
                a = input("Press y or enter to replace, n to skip: ")
            if a == "y" or a == "":
                text = text.replace(word, spellchecker.correction(word))
                print("Replaced")
            else:
                print("Skipped")
            choice[word] = a
            # save to file
            with open("data/choice.pkl", "wb") as f:
                pickle.dump(choice, f)


def correct_mistakes(text, replace_dict):
    for word, replace_word in replace_dict.items():
        text = text.replace(word, replace_word)
    return text


def main_correct(paths):
    # build replace word dict
    spellchecker = SpellChecker()
    replace_dict = {}
    for word, ch in choice.items():
        if ch != "n":
            replace_dict[word] = spellchecker.correction(word)
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            corrected = correct_mistakes(content, replace_dict)
            # save to file follow the original organization
            new_path = output_path + "/" + path
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(corrected)


def main_find(paths):
    # Initialize the spellchecker
    spellchecker = SpellChecker()
    count = 0
    for path in paths:
        count += 1
        file_name = path.split("/")[-1]
        if file_name in checked_files:
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            # Convert markdown to plain text
            # for symbol in symbol_to_replace_list:
            #     content = content.replace(symbol, " ")
            print(f'Checking {count}/{len(paths)} "{file_name}"...')
            annotate_mistakes(content, spellchecker)
            checked_files.append(file_name)
            # save to file
            with open("data/checked_files.pkl", "wb") as f:
                pickle.dump(checked_files, f)


if __name__ == "__main__":
    paths = md_path
    main_correct(paths)
    print(paths)
