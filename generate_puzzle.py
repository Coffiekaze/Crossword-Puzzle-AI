import json
import random
from wordlist_loader import filter_words_from_json

N = 5

filtered = filter_words_from_json("words_dictionary.json", min_length=N, max_length=N)
five_letter_words = [w for w in filtered if len(w) == N]

# Increase pool to 3000–5000 words for better coverage
word_list = random.sample(five_letter_words, min(5000, len(five_letter_words)))

example_grid = ["." * N for _ in range(N)]

puzzle_data = {
    "grid": example_grid,
    "words": word_list
}

with open("puzzle.json", "w", encoding="utf-8") as f:
    json.dump(puzzle_data, f, indent=4)

print(f" puzzle.json created with {len(word_list)} words.")

