import argparse
import json
import sys
from typing import Dict, List, Tuple
import constraint
from wordlist_loader import filter_words_from_json, save_filtered_words

N = 5  # board size (5×5)

class Slot:
    def __init__(self, id_: str, cells: List[Tuple[int, int]]):
        self.id = id_
        self.cells = cells

    def __repr__(self):
        return f"Slot({self.id})"

def validate_grid(grid: List[str]):
    if len(grid) != N or any(len(row) != N for row in grid):
        sys.exit(f"Grid must be {N}×{N}")

def build_slots() -> List[Slot]:
    slots = []
    for r in range(N):
        slots.append(Slot(f"R{r}", [(r, c) for c in range(N)]))
    for c in range(N):
        slots.append(Slot(f"C{c}", [(r, c) for r in range(N)]))
    return slots

def build_problem(grid: List[str], words: List[str], unique: bool):
    solver = constraint.RecursiveBacktrackingSolver()
    problem = constraint.Problem(solver)
    slots = build_slots()

    dictionary = [w.lower() for w in words if len(w) == N]
    if not dictionary:
        sys.exit(f"No {N}‑letter words provided in dictionary.")

    for slot in slots:
        rc, idx = slot.id[0], int(slot.id[1])
        pattern = grid[idx] if rc == 'R' else ''.join(grid[r][idx] for r in range(N))
        domain = dictionary if pattern == '.' * N else [
            w for w in dictionary if all(p == '.' or p == w[i] for i, p in enumerate(pattern))
        ]
        problem.addVariable(slot.id, domain)

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

def to_upper_grid(assign: Dict[str, str]) -> List[str]:
    grid = [[' '] * N for _ in range(N)]
    for r in range(N):
        word = assign[f"R{r}"]
        for c, ch in enumerate(word):
            grid[r][c] = ch.upper()
    return [''.join(row) for row in grid]

# ✅ NEW: This is the function you can use in a GUI
def solve_crossword(puzzle_path="puzzle.json", unique=True) -> str:
    with open(puzzle_path) as fh:
        data = json.load(fh)
    grid = data['grid']
    words = data['words']

    validate_grid(grid)
    problem = build_problem(grid, words, unique)
    solution = problem.getSolution()

    if solution:
        return to_upper_grid(solution)  # <- List of strings like ['HELLO', 'EARTH', ...]
    else:
        return ["." * N for _ in range(N)]  # fallback grid

# --- CLI entry point remains the same ---
def parse_args():
    ap = argparse.ArgumentParser(description="5×5 word‑square solver (python‑constraint)")
    ap.add_argument('puzzle', help='Path to puzzle JSON file')
    ap.add_argument('--unique', action='store_true', help='Enforce all 10 words distinct')
    return ap.parse_args()

def main():
    args = parse_args()
    print(solve_crossword(args.puzzle, unique=args.unique))

if __name__ == '__main__':
    main()
