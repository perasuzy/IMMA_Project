import json, uuid, pulp
from datetime import datetime
from tkinter import messagebox

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

# เขียน function คำนวนในนี้ มีจำนวน total_sofa, total_table, total_chair ให้แล้วจ้า
def calculate_order(orders):
    # โหลดข้อมูล JSON
    with open("pattern.json","r",encoding="utf-8") as f:
        rows = json.load(f)

    # Target ตัวอย่าง
    total_sofa, total_table, total_chair = orders
    target = [total_sofa*4, total_table*4, total_chair*4, total_chair*3]
    print(total_sofa, total_table, total_chair, target)

    # Model
    model = pulp.LpProblem("MinTotalCount", pulp.LpMinimize)
    x_vars = {r["id"]: pulp.LpVariable(f"x_{r['id']}",0,cat="Integer") for r in rows}

    # Constraints >= target
    for i,key in enumerate(["i1","i2","i3","i4"]):
        model += pulp.lpSum(r[key]*x_vars[r["id"]] for r in rows) >= target[i]

    # Objective
    model += pulp.lpSum(x_vars.values())
    model.solve(pulp.PULP_CBC_CMD(msg=0))

    # เก็บผลลัพธ์
    solution = []
    total_used = [0,0,0,0]  # รวม i1,i2,i3,i4
    total_i5 = 0
    total_woods = 0
    for r in rows:
        count = int(x_vars[r["id"]].value() or 0)
        if count>0:
            i5_total = r.get("i5",0) * count
            total_i5 += i5_total
            total_woods += count
            solution.append(f"รูปแบบ {r['id']:02d} [{r['i1']},{r['i2']},{r['i3']},{r['i4']}] {count:02d} ท่อน เหลือเศษ {i5_total:03d} ซม.")
            for i,key in enumerate(["i1","i2","i3","i4"]):
                total_used[i] += r[key]*count

    # แสดงผล pattern
    for s in solution:
        print(s)

    # สรุปเกินเป็น list
    over_list = [max(0,total_used[i]-target[i]) for i in range(4)]
    print("จำนวนไม้ทั้งหมด:", total_woods, "ท่อน")
    print("จำนวนที่เกิน:", over_list)
    print("รวมเศษทั้งหมด:", total_i5, "ซม.")
    return total_woods

