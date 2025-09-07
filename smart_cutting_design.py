from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import json, uuid

# --------------------- Logic ส่วน Data ---------------------
def add_new_order(date, buyer, supplier, sofa, table, chair,add_window):
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []
    
    new_entry = {
        "ID": str(uuid.uuid4()),
        "Date": date,
        "Buyer": buyer,
        "Supplier": supplier,
        "Sofa": sofa,
        "Table": table,
        "Chair": chair,
        "Status": "Inprogress",
        "TimeStamp": ""
    }
    records.append(new_entry)
    
    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    messagebox.showinfo("Submission", "Form Submitted Successfully and saved to orders.json!")
    add_window.destroy()
    

def submit_orders():
    try:
        with open("orders.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            results = [rec for rec in data if rec.get("Status") == "Inprogress"]

            orders = [0,0,0]   # Sofa, Table, Chair
            for result in results:
                orders[0] += int(result["Sofa"])
                orders[1] += int(result["Table"])
                orders[2] += int(result["Chair"])

            total_wood_for_use = calculate_order(orders)
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # update status → Done
            for rec in results:
                rec["Status"] = "Done"
                rec["TimeStamp"] =  time
            with open("orders.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return total_wood_for_use
    except FileNotFoundError:
        messagebox.showerror("Error", "❌ ไม่พบไฟล์ orders.json")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "⚠️ orders.json ไม่ใช่ไฟล์ JSON ที่ถูกต้อง")

def calculate_order(orders):
    total_sofa, total_table, total_chair = orders

    # สูตรคำนวณใช้ไม้
    wood_for_sofa = total_sofa * 1
    wood_for_table = total_table * 1
    wood_for_chair = total_chair * 1

    total_wood = wood_for_sofa + wood_for_table + wood_for_chair
    return total_wood

# --------------------- GUI ส่วนหน้าแรก ---------------------
root = tk.Tk()
root.title("Smart Cutting Design - Main Menu")
root.geometry("300x200")
root.resizable(False, False)

tk.Label(root, text="Smart Cutting Design", font=("Arial", 14, "bold")).pack(pady=20)

def open_add_order_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add New Order")
    add_window.geometry("400x300")

    frame = tk.Frame(add_window)
    frame.pack(pady=10)

    # ฟิลด์กรอกข้อมูล
    labels = ["Date", "Buyer", "Supplier", "Sofa", "Table", "Chair"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=10, pady=2)
        entries[label] = entry

    def submit_action():
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

def open_calculate_order():
    total = submit_orders()
    if total is not None:
        messagebox.showinfo("Total Calculation", f"🌳 Total wood needed: {total}")

def open_history_order():
    history_window = tk.Toplevel(root)
    history_window.title("History Order")
    history_window.geometry("400x300")

    try:
        with open("orders.json", "r") as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    # Listbox แสดง ID ของแต่ละ Order
    listbox = tk.Listbox(history_window, width=50, height=15)
    listbox.pack(pady=10)

    for rec in records:
        listbox.insert(tk.END, f"{rec.get("ID")}")

    def show_detail(event=None):
        try:
            selected_index = listbox.curselection()[0]
            rec = records[selected_index]
        except IndexError:
            messagebox.showwarning("Warning", "กรุณาเลือก Order ก่อน")
            return

        # หน้าต่างรายละเอียด
        detail_window = tk.Toplevel(history_window)
        detail_window.title(f"Order Detail - {rec.get('ID')}")
        detail_window.geometry("400x300")

        detail_text = (
            f"ID: {rec.get('ID')}\n"
            f"Date: {rec.get('Date')}\n"
            f"Buyer: {rec.get('Buyer')}\n"
            f"Supplier: {rec.get('Supplier')}\n"
            f"Sofa: {rec.get('Sofa')}\n"
            f"Table: {rec.get('Table')}\n"
            f"Chair: {rec.get('Chair')}\n"
            f"Status: {rec.get('Status')}\n"
            f"Timestamp: {rec.get('TimeStamp')}\n"
        )

        tk.Label(detail_window, text=detail_text, justify="left", anchor="w").pack(padx=10, pady=10)

    # Double click → เปิดรายละเอียด
    listbox.bind("<Double-Button-1>", show_detail)

    # ปุ่มเปิดรายละเอียด
    view_button = tk.Button(history_window, text="View Detail", command=show_detail)
    view_button.pack(pady=5)

# ปุ่มในหน้าแรก
tk.Button(root, text="➕ เพิ่ม Order      ", width=20, command=open_add_order_window).pack(pady=10)
tk.Button(root, text="📐 Calculate Order", width=20, command=open_calculate_order).pack(pady=10)
tk.Button(root, text="📜 History Order  ", width=20, command=open_history_order).pack(pady=10)


root.mainloop()

