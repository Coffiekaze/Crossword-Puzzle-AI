"""5x5 *word-square* solver

Usage:
    python crossword_solver.py puzzle.json

`puzzle.json` format:
```json
{
  "grid": [
    ".....",
    ".....",
    ".....",
    ".....",
    "....."
  ],
  "words": ["firms", "idiom", "lasso", "cheek", "horsy", "filch", "idaho", "riser", "moses", "smoky"]
}
`.` means an empty cell、prefill has to be lower case.
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple
import constraint
from wordlist_loader import filter_words_from_json, save_filtered_words

N = 5  # board size (5×5)

"""filtered = filter_words_from_json("words_dictionary.json", min_length=4, max_length=7)"""""

# Optional: Save to file
"""save_filtered_words(filtered, "filtered_words.txt")"""

#slot represents one full row or column that must be filled with a single 5-letter word
class Slot:
    """Represents one row (R0‑R4) or column (C0‑C4)."""

    def __init__(self, id_: str, cells: List[Tuple[int, int]]):
        self.id = id_
        self.cells = cells  # always length N

    def __repr__(self):
        return f"Slot({self.id})"


# Helpers

#check if the grid provided is in the right format(5x5)
def validate_grid(grid: List[str]):
    if len(grid) != N or any(len(row) != N for row in grid):
        sys.exit(f"Grid must be {N}×{N}")

#Creates 10 Slot objects (rows R0–R4 and columns C0–C4) and returns them as a list.
def build_slots() -> List[Slot]:
    slots = []
    # Rows R0‑R4
    for r in range(N):
        slots.append(Slot(f"R{r}", [(r, c) for c in range(N)]))
    # Columns C0‑C4
    for c in range(N):
        slots.append(Slot(f"C{c}", [(r, c) for r in range(N)]))
    return slots

#Builds a CSP: assigns domains, adds equality constraints at intersections
def build_problem(grid: List[str], words: List[str], unique: bool):
    solver = constraint.RecursiveBacktrackingSolver()#MRV + forward checking
    problem = constraint.Problem(solver)
    slots = build_slots()

    # 5-letter dictionary
    dictionary = [w.lower() for w in words if len(w) == N]
    if not dictionary:
        sys.exit(f"No {N}‑letter words provided in dictionary.")

    #variables & unary constraints (prefilled patterns)
    for slot in slots:
        #rc is either 'R' or 'C', idex is index 0~4 as an int
        rc, idx = slot.id[0], int(slot.id[1])

        pattern = grid[idx] if rc == 'R' else ''.join(grid[r][idx] for r in range(N))
        # check if there is a prefill
        #it does this by checking if a word in the dictionary fits the exact same index and elements as the word in the pattern
        #if it does then it 
        domain = dictionary if pattern == '.' * N else [w for w in dictionary if all(p == '.' or p == w[i] for i, p in enumerate(pattern))]
        #if there's no prefill, all words in dictionary will be in the domain
        problem.addVariable(slot.id, domain)

    #binary equality constraints at intersections
    cell_map: Dict[Tuple[int, int], List[Tuple[str, int]]] = {}
    for slot in slots:
        for i, cell in enumerate(slot.cells):
            cell_map.setdefault(cell, []).append((slot.id, i))

    for overlaps in cell_map.values():
     if len(overlaps) == 2:
        (s1, i1), (s2, i2) = overlaps
        def same(a, b, i=i1, j=i2):
            return a[i] == b[j]
        problem.addConstraint(same, (s1, s2))

    if unique:
        problem.addConstraint(constraint.AllDifferentConstraint())

    return problem

#Convets the solution mapping into a list of upper case row for display
def to_upper_grid(assign: Dict[str, str]) -> List[str]:
    grid = [[' '] * N for _ in range(N)]
    for r in range(N):
        word = assign[f"R{r}"]
        for c, ch in enumerate(word):
            grid[r][c] = ch.upper()
    return [''.join(row) for row in grid]


#CLI

def parse_args():
    ap = argparse.ArgumentParser(description="5×5 word‑square solver (python‑constraint)")
    ap.add_argument('puzzle', help='Path to puzzle JSON file')
    ap.add_argument('--unique', action='store_true', help='Enforce all 10 words distinct')
    return ap.parse_args()

def main():
    args = parse_args()

    with open(args.puzzle) as fh:
        data = json.load(fh)
    grid = data['grid']
    words = data['words']

    validate_grid(grid)
    problem = build_problem(grid, words, args.unique)
    solution = problem.getSolution()

    if solution:
        for row in to_upper_grid(solution):
            print(row)
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()




