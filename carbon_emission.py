import csv
import importlib
import time
import tkinter as tk

from pathlib import Path
from tkinter import filedialog, messagebox
from codecarbon import EmissionsTracker
from datetime import datetime
from typing import Optional, List, Union

def main() -> None:
    root = tk.Tk()
    app = CarbonEmissionsApp(root)
    root.mainloop()


class CarbonEmissionsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Value Sorter")

        self.start: float = 0.
        self.end: float = 0.

        max_columnspan = 3
        # File selection
        self.file_path: tk.StringVar = tk.StringVar()
        tk.Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)

        # Sorting algorithm selection
        default_implementation_value = "Python"
        self.sorting_implementation = tk.StringVar(value=default_implementation_value)
        tk.Label(root, text="Select Sorting Algorithm:").grid(row=1, column=0, padx=10, pady=10)
        sorting_algorithms = [default_implementation_value, "C++"]
        self.sorting_implementation_menu = tk.OptionMenu(root, self.sorting_implementation, *sorting_algorithms)
        self.sorting_implementation_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Sorting algorithm selection
        default_sorting_value = "Insertion Sort"
        self.sorting_algorithm = tk.StringVar(value=default_sorting_value)
        sorting_algorithms = [default_sorting_value, "Quick Sort", "Heap Sort"]
        self.sorting_algorithm_menu = tk.OptionMenu(root, self.sorting_algorithm, *sorting_algorithms)
        self.sorting_algorithm_menu.grid(row=1, column=1, padx=10, pady=10, sticky='e')

        # Sort button
        tk.Button(root, text="Sort", command=self.sort_names).grid(row=1, column=2,
                                                                                  padx=10, pady=10)
        # Results display
        self.results_text = tk.Text(root, height=20, width=70)
        self.results_text.grid(row=3, column=0, columnspan=max_columnspan, padx=10, pady=10)

        # Timer
        self.timer_label = tk.Label(root, text="Sorting Duration: 0.00 seconds")
        self.timer_label.grid(row=4, column=0, columnspan=max_columnspan, padx=10, pady=10)

    def update_timer(self, duration: float):
        self.timer_label.config(text=f"Sorting Duration: {duration:.6f} seconds")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
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
            sorted_data = self.load_and_sort_values(self.file_path.get())
            self.update_timer(self.end - self.start)
            self.display_values_names(sorted_data)
            self.write_sorting_info()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def determine_expected_type(self, value: str) -> type:
        if value.isdigit():
            return int
        try:
            float(value)
            return float
        except ValueError:
            return str

    def load_file(self, file_path: str) -> Optional[List]:
        try:
            path = Path(file_path)
            file_ext = path.suffix.lower()

            if file_ext != '.csv':
                messagebox.showerror("Error", f"Unsupported file format: {file_ext}")
                return None

            result: List[Union[int, float, str]] = []
            with (open(path, mode='r', newline='') as file):
                reader = csv.reader(file)
                first_entry = next(reader)
                expected_type = self.determine_expected_type(first_entry[0])
                file.seek(0)

                for row in reader:
                    if len(row) != 1:
                        raise Exception(f"Unexpected row length: Expected a length of 1 but got {len(row)}")
                    try:
                        if expected_type is int:
                            result.append(int(row[0]))
                        elif expected_type is float:
                            result.append(float(row[0]))
                        else:
                            result.append(row[0])
                    except ValueError:
                        raise Exception(
                            f"Unexpected value type: Expected either int, float or string, instead got {type(row[0])}")
            return result

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found at {file_path}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def load_and_sort_values(self, file_path: str) -> List | None:
        try:
            data = self.load_file(file_path)

            if not data or len(data) == 0:
                messagebox.showerror("Error", f"Unable to load data contents")
                return None

            implementation = self.sorting_implementation.get()
            algorithm = self.sorting_algorithm.get().lower().replace(' ', '_')
            if implementation == "Python":
                module_name = "py.sort.sort"
            elif implementation == "C++":
                module_name = "cpp.sort.sorting_algorithms"
            else:
                raise ValueError(f"Unsupported implementation: {implementation}")

            sort_module = importlib.import_module(module_name)
            sort_function = getattr(sort_module, algorithm)

            with EmissionsTracker() as tracker:
                self.start = time.time()
                result = sort_function(data)
                self.end = time.time()

            return result

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def display_values_names(self, data: List):
        if data is None:
            self.results_text.insert(tk.END, "No data to display.")
            return

        self.results_text.insert(tk.END, "\tSorted data:\n")
        self.results_text.insert(tk.END, "------------------------------------\n")

        for n, value in enumerate(data, start=1):
            self.results_text.insert(tk.END, f"{n}:\t{value}\n")

    def write_sorting_info(self):
        duration = (self.end - self.start) * 1000. # to milliseconds
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("results/sorting_info.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                Path(self.file_path.get()).name,
                self.sorting_implementation.get(),
                self.sorting_algorithm.get(),
                f"{duration:.16f}"])


if __name__ == "__main__":
    main()
