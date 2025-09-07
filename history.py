import tkinter as tk
from tkinter import messagebox
from utils import calculate_order, read_data

# ------------------- ฟังก์ชันเปิด History Order -------------------
def open_history_order(root):
    history_window = tk.Toplevel(root)
    history_window.title("History Order")
    history_window.geometry("500x400")

    records = read_data()

    # สร้าง mapping: timestamp → list ของ order
    timestamp_map = {}
    for rec in records:
        ts = rec.get("IDCalculate")
        if ts not in timestamp_map:
            timestamp_map[ts] = []
        timestamp_map[ts].append(rec)

    # Listbox แสดง Timestamp + จำนวน order + Status
    listbox = tk.Listbox(history_window, width=60, height=15)
    listbox.pack(pady=10)

    for ts, orders in sorted(timestamp_map.items()):
        count = len(orders)
        statuses = set(o.get("Status") for o in orders)
        status_text = "/".join(statuses)
        listbox.insert(tk.END, f"{ts} ({count} order{'s' if count>1 else ''}, {status_text})")

    # Event Double click → เปิดรายละเอียด
    def on_double_click(event):
        try:
            selected_index = listbox.curselection()[0]
            selected_text = listbox.get(selected_index)
            selected_ts = selected_text.split(" (")[0]
            show_detail(timestamp_map, selected_ts, parent=history_window)
        except IndexError:
            messagebox.showwarning("Warning", "กรุณาเลือก Timestamp ก่อน")

    listbox.bind("<Double-Button-1>", on_double_click)

    # ปุ่ม View Detail
    def on_view_button():
        try:
            selected_index = listbox.curselection()[0]
            selected_text = listbox.get(selected_index)
            selected_ts = selected_text.split(" (")[0]
            show_detail(timestamp_map, selected_ts, parent=history_window)
        except IndexError:
            messagebox.showwarning("Warning", "กรุณาเลือก Timestamp ก่อน")

    tk.Button(history_window, text="View Detail", command=on_view_button).pack(pady=5)


# ------------------- ฟังก์ชันแยก show_detail -------------------
def show_detail(timestamp_map, selected_ts=None, parent=None):
    if selected_ts is None:
        messagebox.showwarning("Warning", "กรุณาเลือก Timestamp ก่อน")
        return

    orders_to_show = timestamp_map.get(selected_ts, [])
    if not orders_to_show:
        messagebox.showinfo("Info", "ไม่มี order สำหรับ Timestamp นี้")
        return

    # สร้างหน้าต่างรายละเอียด
    detail_window = tk.Toplevel(parent)
    detail_window.title(f"Orders at {selected_ts}")
    detail_window.geometry("500x400")

    text_box = tk.Text(detail_window, wrap="word", width=60, height=25)
    text_box.pack(padx=10, pady=10)
    orders = [0, 0, 0]   # Sofa, Table, Chair
    for n, rec in enumerate(orders_to_show, start=1):
        detail_text = (
            f"{'-'*15} Order {n} {'-'*16}\n"
            # f"ID: {rec.get('ID')}\n"
            f"Date: \t{rec.get('Date')}\n"
            f"Buyer: \t{rec.get('Buyer')}\n"
            # f"Supplier: {rec.get('Supplier')}\n"
            f"Sofa: \t{rec.get('Sofa')}\n"
            f"Table: \t{rec.get('Table')}\n"
            f"Chair: \t{rec.get('Chair')}\n"
            # f"Status: {rec.get('Status')}\n"
            f"Time: \t{rec.get('TimeStamp')}\n"
        )
        orders[0] += int(rec.get('Sofa'))
        orders[1] += int(rec.get('Table'))
        orders[2] += int(rec.get('Chair'))
        text_box.insert(tk.END, detail_text)

    text_box.insert(tk.END, f"{'-'*12} Summary Order {'-'*13}\n Sofa: {orders[0]}\n Table: {orders[1]}\n Chair: {orders[2]}\n Total Wood: {calculate_order(orders)}")
    text_box.config(state="disabled")

