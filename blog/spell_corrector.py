import pickle
from spellchecker import SpellChecker

with open("data/choice.pkl", "rb") as f:
    choice_dict = pickle.load(f)
spellchecker = SpellChecker()
replace_words = []
for words, choice in choice_dict.items():
    if choice != "n":
        print(words, choice, spellchecker.correction(words))
        replace_words.append(words)
print(len(replace_words))
