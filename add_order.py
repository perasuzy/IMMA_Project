import tkinter as tk
from tkcalendar import DateEntry  # ต้องติดตั้งด้วย pip install tkcalendar
from tkinter import messagebox
from utils import add_new_order, calculate_order
import json, uuid, pulp
from datetime import datetime
from utils import *

def open_add_order_window(root):
    add_window = tk.Toplevel(root)
    add_window.title("Add New Order")
    add_window.geometry("400x300")

    frame = tk.Frame(add_window)
    frame.pack(pady=10)

    labels = ["Date", "Buyer", "Supplier", "Sofa", "Table", "Chair"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        if label == "Date":
            entry = DateEntry(frame, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        else:
            entry = tk.Entry(frame)

        entry.grid(row=i, column=1, padx=10, pady=2)
        entries[label] = entry

    def submit_action():
        # 1) ตรวจสอบว่ามีช่องไหนเว้นว่างบ้าง
        empty_fields = [label for label, entry in entries.items() if not entry.get().strip()]
        if empty_fields:
            messagebox.showerror("Error", f"กรุณากรอกข้อมูลให้ครบทุกช่อง\nเว้นว่าง: {', '.join(empty_fields)}")
            return

        # 2) ตรวจสอบว่า Sofa, Table, Chair ต้องเป็นตัวเลขเท่านั้น
        for field in ["Sofa", "Table", "Chair"]:
            value = entries[field].get().strip()
            if not value.isdigit():
                messagebox.showerror("Error", f"{field} ต้องเป็นตัวเลขเท่านั้น")
                return
        add_new_order(
            entries["Date"].get(),
            entries["Buyer"].get(),
            entries["Supplier"].get(),
            entries["Sofa"].get(),
            entries["Table"].get(),
            entries["Chair"].get(),
            add_window
        )

    tk.Button(add_window, text="Submit", command=submit_action).pack(pady=10)
