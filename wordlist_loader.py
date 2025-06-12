import json
import os

#def load_words(filename="scowl/english-words.60", min_length=3, max_length=15):
   # with open(filename, "r", encoding="utf-8") as f:
      #  return [
    #        word.strip().lower()
       #     for word in f
     #       if word.isalpha()
    #        and min_length <= len(word.strip()) <= max_length
       # ]
# Load the word dictionary
def filter_words_from_json(json_path, min_length=3, max_length=7):
    with open(json_path, "r", encoding="utf-8") as file:
        words_dict = json.load(file)

    filtered = [
        word for word in words_dict
        if word.isalpha()
        and word.islower()
        and min_length <= len(word) <= max_length
    ]

    return filtered

def save_filtered_words(filtered_words, output_path="filtered_words.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        for word in filtered_words:
            f.write(word + "\n")