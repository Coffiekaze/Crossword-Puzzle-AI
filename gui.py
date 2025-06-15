import tkinter as tk
from tkinter import messagebox
import crosswordSolver

cell_labels = []

def run_solver():
    try:
        result = crosswordSolver.solve_crossword("puzzle.json", unique=True)
        grid_size = len(result)
        build_grid(grid_size)

        for r in range(grid_size):
            for c in range(grid_size):
                char = result[r][c]
                label = cell_labels[r][c]
                if char == ".":
                    label.config(text="", bg="black")
                else:
                    label.config(text=char.upper(), bg="white", fg="black")

        status_label.config(text="✅ Puzzle solved!", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to solve puzzle:\n{e}")
        status_label.config(text="❌ Error solving puzzle", fg="red")

def build_grid(size):
    for widget in grid_frame.winfo_children():
        widget.destroy()

    cell_labels.clear()

    for r in range(size):
        row = []
        for c in range(size):
            label = tk.Label(grid_frame, text="", width=4, height=2,
                             font=("Courier New", 24, "bold"),
                             bg="white", fg="black", relief="solid", bd=1)
            label.grid(row=r, column=c, padx=2, pady=2)
            row.append(label)
        cell_labels.append(row)

# === GUI Setup ===
root = tk.Tk()
root.title("Crossword Puzzle Solver")
root.geometry("600x650")
root.config(bg="#f0f4f7")

frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
frame.pack(padx=20, pady=20, fill="both", expand=True)

title_label = tk.Label(frame, text="🧩 Crossword Puzzle Solver", font=("Helvetica", 18, "bold"), bg="#ffffff")
title_label.pack(pady=(0, 10))

grid_frame = tk.Frame(frame, bg="#ffffff")
grid_frame.pack(pady=10)

solve_button = tk.Button(
    frame,
    text="🔍 Solve Puzzle",
    font=("Helvetica", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="raised",
    cursor="hand2",
    command=run_solver
)
solve_button.pack(pady=20)

status_label = tk.Label(frame, text="", font=("Helvetica", 10, "italic"), bg="#ffffff", fg="gray")
status_label.pack(pady=(5, 0))

root.mainloop()
