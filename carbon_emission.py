import codecarbon
import tkinter as tk
import pandas as pd

from pathlib import Path
from tkinter import filedialog, messagebox
from codecarbon import OfflineEmissionsTracker


def main() -> None:
    root = tk.Tk()
    app = NameSorterApp(root)
    root.mainloop()


class NameSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Name Sorter")

        # File selection
        self.file_path = tk.StringVar()
        tk.Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)

        # Sort button
        tk.Button(root, text="Sort Names by Count", command=self.sort_names).grid(row=1, column=0, columnspan=3,
                                                                                  padx=10, pady=10)

        # Results display
        self.results_text = tk.Text(root, height=20, width=70)
        self.results_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx")]
        )
        if file_path:
            self.file_path.set(file_path)

    def sort_names(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        try:
            self.results_text.delete(1.0, tk.END)

            sorted_df = self.load_and_sort_names(file_path)

            if sorted_df is None:
                return

            self.display_sorted_names(sorted_df)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_and_sort_names(self, file_path):
        try:
            # Determine file type based on extension
            file_ext = Path(file_path).suffix.lower()

            # Read the file based on its extension
            if file_ext == '.csv':
                df = pd.read_csv(file_path, header=None, usecols=[0, 1], names=['Name', 'Count'], dtype={'Name': str, 'Count': str})
            elif file_ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path, header=None, usecols=[0, 1], names=['Name', 'Count'])
            else:
                messagebox.showerror("Error", f"Unsupported file format: {file_ext}")
                return None

            df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
            df = df.dropna(subset=['Count'])
            df['Count'] = df['Count'].astype(int)

            with OfflineEmissionsTracker() as tracker:
                df_sorted = df.sort_values(by='Count', ascending=False)

            # Reset index to have a clean output
            df_sorted = df_sorted.reset_index(drop=True)

            return df_sorted

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found at {file_path}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def display_sorted_names(self, df):
        if df is None:
            self.results_text.insert(tk.END, "No data to display.")
            return

        self.results_text.insert(tk.END, "Names sorted by count (descending):\n")
        self.results_text.insert(tk.END, "------------------------------------\n")
        self.results_text.insert(tk.END, f"{'Rank':<6} {'Name':<20} {'Count':<10}\n")
        self.results_text.insert(tk.END, "------------------------------------\n")

        for index, row in df.iterrows():
            self.results_text.insert(tk.END, f"{index + 1:<6} {row['Name']:<20} {row['Count']:<10}\n")


if __name__ == "__main__":
    main()
