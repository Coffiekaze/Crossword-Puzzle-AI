import tkinter as tk
from tkinter import messagebox, simpledialog
import crosswordSolver
import subprocess
import json

cell_labels = []
prefill_grid = []
words = []

# --- Core Functions ---
def generate_puzzle():
    # Run puzzle generator
    subprocess.run(["python", "generate_puzzle.py"], check=True)
    # Load generated puzzle
    with open("puzzle.json") as fh:
        data = json.load(fh)
    return data['grid'], data['words']


def build_grid(size):
    # Clear existing grid
    for widget in grid_frame.winfo_children():
        widget.destroy()
    cell_labels.clear()

    # Initialize labels matrix and prefill grid
    global prefill_grid
    prefill_grid = [['.' for _ in range(size)] for _ in range(size)]

    for r in range(size):
        row = []
        for c in range(size):
            label = tk.Label(
                grid_frame,
                text="",
                width=4,
                height=2,
                font=("Courier New", 24, "bold"),
                bg="black",
                fg="white",
                relief="solid",
                bd=1
            )
            label.grid(row=r, column=c, padx=2, pady=2)
            # Bind click for prefill mode
            label.bind(
                "<Button-1>",
                lambda e, rr=r, cc=c: on_cell_click(rr, cc)
            )
            row.append(label)
        cell_labels.append(row)


def on_cell_click(r, c):
    # Prompt user for a letter
    letter = simpledialog.askstring(
        "Input Letter",
        f"Enter letter for cell ({r}, {c}):"
    )
    if letter and len(letter) == 1 and letter.isalpha():
        letter = letter.lower()
        prefill_grid[r][c] = letter
        label = cell_labels[r][c]
        label.config(text=letter.upper(), bg="white", fg="black")
    else:
        messagebox.showwarning("Invalid", "Please enter a single letter.")


def start_prefill_mode():
    try:
        grid, loaded_words = generate_puzzle()
        global words
        words = loaded_words
        size = len(grid)
        build_grid(size)
        status_label.config(
            text=" Prefill letters by clicking on cells, then click 'Solve Prefilled Puzzle'",
            fg="blue"
        )
        solve_prefill_button.pack(pady=(10, 0))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to generate puzzle:\n{e}")


def solve_prefilled():
    try:
        # Overwrite the real puzzle.json with the prefilled grid
        puzzle_data = {
            'grid': [''.join(row) for row in prefill_grid],
            'words': words
        }
        with open("puzzle.json", "w") as fh:
            json.dump(puzzle_data, fh)

        # Solve CSP on the updated puzzle.json
        result = crosswordSolver.solve_crossword("puzzle.json", unique=True)
        size = len(result)

        # Display solution
        for r in range(size):
            for c in range(size):
                char = result[r][c]
                label = cell_labels[r][c]
                if char == ".":
                    label.config(text="", bg="black")
                else:
                    label.config(text=char.upper(), bg="white", fg="black")

        status_label.config(text="Prefilled puzzle solved!", fg="green")
        solve_prefill_button.pack_forget()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to solve prefilled puzzle:\n{e}")
        status_label.config(text=" Error solving prefilled puzzle", fg="red")



def run_solver():
    # Standard solve (generate + solve)
    try:
        subprocess.run(["python", "generate_puzzle.py"], check=True)
        result = crosswordSolver.solve_crossword("puzzle.json", unique=True)
        size = len(result)
        build_grid(size)

        for r in range(size):
            for c in range(size):
                char = result[r][c]
                label = cell_labels[r][c]
                if char == ".":
                    label.config(text="", bg="black")
                else:
                    label.config(text=char.upper(), bg="white", fg="black")

        status_label.config(text=" Puzzle generated & solved!", fg="green")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to generate puzzle:\n{e}")
        status_label.config(text="Error generating puzzle", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to solve puzzle:\n{e}")
        status_label.config(text=" Error solving puzzle", fg="red")

# === GUI Setup ===
root = tk.Tk()
root.title("Crossword Puzzle Solver")
root.geometry("600x750")
root.config(bg="#f0f4f7")

frame = tk.Frame(
    root,
    bg="#ffffff",
    bd=2,
    relief="groove",
    padx=20,
    pady=20
)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title
title_label = tk.Label(
    frame,
    text=" Crossword Puzzle Solver",
    font=("Helvetica", 18, "bold"),
    bg="#ffffff"
)
title_label.pack(pady=(0, 10))

# Grid container
grid_frame = tk.Frame(frame, bg="#ffffff")
grid_frame.pack(pady=10)

# Buttons
solve_button = tk.Button(
    frame,
    text="🔍 Generate & Solve Puzzle",
    font=("Helvetica", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="raised",
    cursor="hand2",
    command=run_solver
)
solve_button.pack(pady=5)

prefill_button = tk.Button(
    frame,
    text="Prefill & Solve Puzzle",
    font=("Helvetica", 12, "bold"),
    bg="#FF9800",
    fg="white",
    activebackground="#FB8C00",
    relief="raised",
    cursor="hand2",
    command=start_prefill_mode
)
prefill_button.pack(pady=5)

solve_prefill_button = tk.Button(
    frame,
    text=" Solve Prefilled Puzzle",
    font=("Helvetica", 12, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1e88e5",
    relief="raised",
    cursor="hand2",
    command=solve_prefilled
)
# Do not pack solve_prefill_button now; it's shown in prefill mode

# Status label
status_label = tk.Label(
    frame,
    text="",
    font=("Helvetica", 10, "italic"),
    bg="#ffffff",
    fg="gray"
)
status_label.pack(pady=(10, 0))

root.mainloop()
