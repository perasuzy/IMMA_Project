import tkinter as tk
from add_order import open_add_order_window
from calculate import open_calculate_order
from history import open_history_order

root = tk.Tk()
root.title("Smart Cutting Design - Main Menu")
root.geometry("300x200")
root.resizable(False, False)

tk.Label(root, text="Smart Cutting Design", font=("Arial", 14, "bold")).pack(pady=20)

# ปุ่มในหน้าแรก
tk.Button(root, text="➕ เพิ่ม Order      ", width=20, command=lambda: open_add_order_window(root)).pack(pady=10)
tk.Button(root, text="📐 Calculate Order", width=20, command=open_calculate_order).pack(pady=10)
tk.Button(root, text="📜 History Order  ", width=20, command=lambda: open_history_order(root)).pack(pady=10)

root.mainloop() 


#