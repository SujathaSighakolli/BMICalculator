import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

# File to store BMI history
DATA_FILE = "bmi_history.json"

# Load existing history
def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save new entry to history
def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(DATA_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Calculate BMI and display result
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if height <= 0 or weight <= 0:
            raise ValueError

        bmi = round(weight / (height * height), 2)

        if bmi < 18.5:
            category = "Underweight 🥗"
        elif 18.5 <= bmi < 24.9:
            category = "Normal 💪"
        elif 25 <= bmi < 29.9:
            category = "Overweight 🍔"
        else:
            category = "Obese ⚠️"

        result_label.config(text=f"BMI: {bmi}\nCategory: {category}", foreground="#003366")

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "category": category
        }
        save_history(entry)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric weight and height values.")

# View history in a new window
def view_history():
    history = load_history()
    if not history:
        messagebox.showinfo("History", "No data available yet.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("500x300")
    history_window.config(bg="#f0f0ff")

    tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (m)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")

    for entry in history:
        tree.insert("", tk.END, values=(entry["date"], entry["weight"], entry["height"], entry["bmi"], entry["category"]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

# Plot BMI trend
def show_graph():
    history = load_history()
    if len(history) < 2:
        messagebox.showinfo("Graph", "At least 2 entries required to show trend.")
        return

    dates = [entry["date"] for entry in history]
    bmis = [entry["bmi"] for entry in history]

    plt.figure(figsize=(6, 4))
    plt.plot(dates, bmis, marker="o", color="blue")
    plt.title("BMI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x400")
root.config(bg="#dbefff")

title_label = tk.Label(root, text="BMI CALCULATOR", font=("Arial Rounded MT Bold", 20), fg="#003366", bg="#dbefff")
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#dbefff")
frame.pack(pady=10)

tk.Label(frame, text="Enter weight (kg):", font=("Segoe UI", 12), bg="#dbefff").grid(row=0, column=0, padx=5, pady=5)
weight_entry = tk.Entry(frame, font=("Segoe UI", 12))
weight_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Enter height (m):", font=("Segoe UI", 12), bg="#dbefff").grid(row=1, column=0, padx=5, pady=5)
height_entry = tk.Entry(frame, font=("Segoe UI", 12))
height_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Calculate BMI", font=("Segoe UI", 12, "bold"), bg="#003366", fg="white", command=calculate_bmi).pack(pady=10)
result_label = tk.Label(root, text="", font=("Segoe UI", 13), bg="#dbefff")
result_label.pack(pady=5)

tk.Button(root, text="View History", font=("Segoe UI", 11), bg="#aad8ff", command=view_history).pack(pady=5)
tk.Button(root, text="Show BMI Graph", font=("Segoe UI", 11), bg="#aad8ff", command=show_graph).pack(pady=5)

root.mainloop()
