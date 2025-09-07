from tkinter import messagebox
from utils import submit_orders

def open_calculate_order():
    total = submit_orders()
    if total is not None:
        messagebox.showinfo("Total Calculation", f"🌳 Total wood needed: {total}")
