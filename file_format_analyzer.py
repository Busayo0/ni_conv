import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
import chardet
import os
import threading
import time
import random

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
        return pan_value

def process_file(file_path, status_label, progress_bar, canvas):
    try:
        status_label.config(text="Reading file... Please wait ⏳")
        progress_bar['value'] = 10
        time.sleep(0.5)

        encoding = detect_encoding(file_path)
        df = pd.read_csv(file_path, delimiter='|', encoding=encoding, dtype=str)

        if df.empty:
            status_label.config(text="")
            messagebox.showerror("Error", "The file is empty or unreadable.")
            return

        pan_column = df.columns[0]
        sample_value = df[pan_column].iloc[0]

        if not (sample_value.isdigit() and 12 <= len(sample_value) <= 19):
            pan_column = simpledialog.askstring(
                "Select Column",
                f"Default first column doesn't look like a PAN.
Enter the correct column name to mask:

{list(df.columns)}"
            )
            if pan_column not in df.columns:
                status_label.config(text="")
                messagebox.showerror("Error", "Invalid column name selected.")
                return

        status_label.config(text="Masking PAN data... 🍳 Cooking in progress...")
        progress_bar['value'] = 40
        df[pan_column] = df[pan_column].apply(mask_pan)

        status_label.config(text="Almost done... preparing download options.")
        progress_bar['value'] = 70
        time.sleep(1)

        save_file(df, progress_bar, canvas)
        status_label.config(text="Done! 🎉")

    except Exception as e:
        status_label.config(text="")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_file(status_label, progress_bar, canvas):
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        threading.Thread(target=process_file, args=(file_path, status_label, progress_bar, canvas)).start()

def save_file(df, progress_bar, canvas):
    file_types = [("CSV files", "*.csv"), ("JSON files", "*.json")]
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=file_types,
        title="Save As"
    )
    if save_path:
        df_with_blank = pd.concat([pd.DataFrame([[""] * len(df.columns)], columns=df.columns), df], ignore_index=True)
        if save_path.endswith('.csv'):
            df_with_blank.to_csv(save_path, index=False)
        elif save_path.endswith('.json'):
            df.to_json(save_path, orient='records', indent=4)

        progress_bar['value'] = 100
        launch_confetti(canvas)
        messagebox.showinfo("Success", f"File saved successfully to:
{save_path}")

def launch_confetti(canvas):
    for _ in range(100):
        x = random.randint(10, 380)
        y = random.randint(10, 200)
        size = random.randint(5, 10)
        color = random.choice(["red", "blue", "green", "purple", "orange", "gold"])
        canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
    canvas.after(1500, canvas.delete, "all")  # clear after 1.5s

def create_app():
    root = tk.Tk()
    root.title("Finconv File Format Analyzer")
    root.geometry("440x360")

    label = tk.Label(root, text="Finconv Format Analyzer", font=("Arial", 18))
    label.pack(pady=10)

    status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
    status_label.pack(pady=5)

    progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
    progress_bar.pack(pady=5)

    select_button = tk.Button(root, text="Select File", command=lambda: select_file(status_label, progress_bar, canvas), height=2, width=25)
    select_button.pack(pady=10)

    footer_label = tk.Label(root, text="Parse • Mask PAN • Save as CSV/JSON", font=("Arial", 9))
    footer_label.pack(pady=10)

    canvas = tk.Canvas(root, width=400, height=100, bg="white", highlightthickness=1, highlightbackground="lightgray")
    canvas.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_app()
    
