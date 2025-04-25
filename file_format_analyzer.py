import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import chardet
import os

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def mask_pan(pan_value):
    if not isinstance(pan_value, str):
        pan_value = str(pan_value)
    if len(pan_value) >= 8:
        return pan_value[:4] + '*' * (len(pan_value) - 8) + pan_value[-4:]
    else:
        return pan_value  # Leave it unmasked if too short

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        process_file(file_path)

def process_file(file_path):
    try:
        encoding = detect_encoding(file_path)
        df = pd.read_csv(file_path, delimiter='|', encoding=encoding, dtype=str)

        if df.empty:
            messagebox.showerror("Error", "The file is empty or unreadable.")
            return

        # Try to detect default PAN column
        pan_column = df.columns[0]
        sample_value = df[pan_column].iloc[0]

        if not (sample_value.isdigit() and 12 <= len(sample_value) <= 19):
            # If not PAN-like, ask user to select
            pan_column = simpledialog.askstring(
                "Select Column",
                f"Default first column doesn't look like a PAN.\nEnter the correct column name to mask:\n\n{list(df.columns)}"
            )
            if pan_column not in df.columns:
                messagebox.showerror("Error", "Invalid column name selected.")
                return

        # Mask the PAN column
        df[pan_column] = df[pan_column].apply(mask_pan)

        # Ask user where to save
        save_file(df)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def save_file(df):
    file_types = [("CSV files", "*.csv"), ("JSON files", "*.json")]
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=file_types,
        title="Save As"
    )
    if save_path:
        if save_path.endswith('.csv'):
            df.to_csv(save_path, index=False)
        elif save_path.endswith('.json'):
            df.to_json(save_path, orient='records', indent=4)
        else:
            messagebox.showerror("Error", "Unsupported file format selected.")
            return

        messagebox.showinfo("Success", f"File saved successfully to:\n{save_path}")

def create_app():
    root = tk.Tk()
    root.title("Finconv File Format Analyzer")
    root.geometry("400x250")

    label = tk.Label(root, text="Finconv Format Analyzer", font=("Arial", 18))
    label.pack(pady=20)

    select_button = tk.Button(root, text="Select File", command=select_file, height=2, width=20)
    select_button.pack(pady=10)

    info_label = tk.Label(root, text="Parse • Mask PAN • Save as CSV/JSON", font=("Arial", 10))
    info_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_app()
