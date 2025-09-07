import tkinter as tk
from tkcalendar import DateEntry  # ต้องติดตั้งด้วย pip install tkcalendar
from tkinter import messagebox
from utils import add_new_order, calculate_order
import json, uuid, pulp
from datetime import datetime

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

def read_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_data(records):
    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

def add_new_order(date, buyer, supplier, sofa, table, chair, add_window):
    records = read_data()
    new_entry = {
        "ID": str(uuid.uuid4()),
        "IDCalculate": "",
        "Date": date,
        "Buyer": buyer,
        "Supplier": supplier,
        "Sofa": sofa,
        "Table": table,
        "Chair": chair,
        "Status": "Inprogress",
        "TimeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    records.append(new_entry)
    write_data(records)
    messagebox.showinfo("Submission", "Form Submitted Successfully and saved to orders.json!")
    add_window.destroy()

def submit_orders():
    data = read_data()
    results = [rec for rec in data if rec.get("Status") == "Inprogress"]

    orders = [0, 0, 0]   # Sofa, Table, Chair
    for result in results:
        orders[0] += int(result["Sofa"])
        orders[1] += int(result["Table"])
        orders[2] += int(result["Chair"])

    total_wood_for_use = calculate_order(orders)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    IDCalculate = time.replace("-", "").replace(" ", "").replace(":", "")

    for rec in results:
        rec["Status"] = "Done"
        rec["IDCalculate"] = IDCalculate  # <-- string
        rec["TimeStamp"] = time
    write_data(data)
    return total_wood_for_use
