import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from pathlib import Path

class DataPreprocessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Preprocessor")

        self.input_file_path = tk.StringVar()
        tk.Label(root, text="Select Input File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.input_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_input_file).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(root, text="Preprocess Data", command=self.preprocess_data).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx")]
        )
        if file_path:
            self.input_file_path.set(file_path)

    def preprocess_data(self):
        input_file = self.input_file_path.get()
        if not input_file:
            messagebox.showerror("Error", "Please select an input file first.")
            return

        try:
            file_ext = Path(input_file).suffix.lower()

            if file_ext == '.csv':
                df = pd.read_csv(input_file, header=None, usecols=[0, 2],  # First and third columns
                                names=['Name', 'Count'],
                                dtype={'Name': str, 'Count': str})
            elif file_ext in ['.xls', '.xlsx']:
                df = pd.read_excel(input_file, header=None, usecols=[0, 2],  # First and third columns
                                  names=['Name', 'Count'],
                                  dtype={'Name': str, 'Count': str})
            else:
                messagebox.showerror("Error", f"Unsupported file format: {file_ext}")
                return

            df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
            df = df.dropna(subset=['Count'])
            df['Count'] = df['Count'].astype(int)
            df = df.sample(frac=1, random_state=42).reset_index(drop=True)

            output_file = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                initialfile=f"{Path(input_file).stem}_shuffled.csv",
                title="Save Preprocessed Data"
            )

            if output_file:
                df.to_csv(output_file, index=False)
                self.status_label.config(text=f"Success: Data preprocessed and saved to {output_file}", fg="green")
            else:
                self.status_label.config(text="Operation cancelled by user.", fg="orange")

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found at {input_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPreprocessorApp(root)
    root.mainloop()
