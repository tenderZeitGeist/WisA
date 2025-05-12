import time
import tkinter as tk
import pandas as pd

from pathlib import Path
from tkinter import filedialog, messagebox
from codecarbon import EmissionsTracker
from typing import Dict, Optional

from pandas import DataFrame


def main() -> None:
    root = tk.Tk()
    app = NameSorterApp(root)
    root.mainloop()


class NameSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Name Sorter")

        self.start: float = 0.
        self.end: float = 0.

        # File selection
        self.file_path: tk.StringVar = tk.StringVar()
        tk.Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)

        # Sorting algorithm selection
        self.sorting_algorithm = tk.StringVar(value="Default")
        tk.Label(root, text="Select Sorting Algorithm:").grid(row=1, column=0, padx=10, pady=10)
        sorting_algorithms = ["Default", "Merge Sort", "Heap Sort"]
        self.sorting_menu = tk.OptionMenu(root, self.sorting_algorithm, *sorting_algorithms)
        self.sorting_menu.grid(row=1, column=1, padx=10, pady=10)

        # Sort button
        tk.Button(root, text="Sort Names by Count", command=self.sort_names).grid(row=1, column=2,
                                                                                  padx=10, pady=10)
        # Results display
        self.results_text = tk.Text(root, height=20, width=70)
        self.results_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Timer
        self.timer_label = tk.Label(root, text="Sorting Duration: 0.00 seconds")
        self.timer_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def update_timer(self, duration: float):
        self.timer_label.config(text=f"Sorting Duration: {duration:.2f} seconds")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx")]
        )
        if not file_path:
            return
        self.file_path.set(file_path)

    def sort_names(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        try:
            self.results_text.delete(1.0, tk.END)
            sorted_df = self.load_and_sort_names(self.file_path.get())
            self.update_timer(self.end - self.start)
            self.display_sorted_names(sorted_df)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_file(self, file_path: str) -> Dict | None:
        try :
            file_ext = Path(file_path).suffix.lower()

            if file_ext == '.csv':
                df = pd.read_csv(file_path, header=None, usecols=[0, 1], names=['Name', 'Count'],
                                dtype={'Name': str, 'Count': str})
            elif file_ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path, header=None, usecols=[0, 1], names=['Name', 'Count'])
            else:
                messagebox.showerror("Error", f"Unsupported file format: {file_ext}")
                return None

            df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
            df = df.dropna(subset=['Count'])
            df['Count'] = df['Count'].astype(int)

            return df.set_index('Name')['Count'].to_dict()

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found at {file_path}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def load_and_sort_names(self, file_path: str) -> DataFrame | None:
        try:
            data = self.load_file(file_path)

            with EmissionsTracker() as tracker:
                self.start = time.time()
                result = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
                self.end = time.time()

            return result

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def display_sorted_names(self, data: Dict):
        if data is None:
            self.results_text.insert(tk.END, "No data to display.")
            return

        self.results_text.insert(tk.END, "Names sorted by count (descending):\n")
        self.results_text.insert(tk.END, "------------------------------------\n")
        self.results_text.insert(tk.END, f"{'Rank':<6} {'Name':<20} {'Count':<10}\n")
        self.results_text.insert(tk.END, "------------------------------------\n")

        for rank, (name, count) in enumerate(data.items(), start=1):
            self.results_text.insert(tk.END, f"{rank:<6} {name:<20} {count:<10}\n")


if __name__ == "__main__":
    main()
