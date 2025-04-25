import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import chardet
import os

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def analyze_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt *.csv"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        encoding = detect_encoding(file_path)
        df = pd.read_csv(file_path, encoding=encoding)

        num_columns = len(df.columns)
        num_rows = len(df)

        messagebox.showinfo(
            "Analysis Result",
            f"✅ File Loaded Successfully!\n\nRows: {num_rows}\nColumns: {num_columns}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"❌ Could not process the file.\n\nError: {str(e)}"
        )

def create_app():
    root = tk.Tk()
    root.title("Finconv File Format Analyzer")
    root.geometry("400x200")

    label = tk.Label(root, text="Welcome to Finconv Analyzer", font=("Arial", 16))
    label.pack(pady=20)

    analyze_button = tk.Button(root, text="Select File and Analyze", command=analyze_file, height=2, width=25)
    analyze_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()
