import json

# โหลด JSON เดิม
with open("pattern.json", "r", encoding="utf-8") as f:
    rows = json.load(f)

# ค่าใหม่ที่จะเพิ่มเป็น i5
i5_values = [
    25,15,15,15,15,15,5,5,5,5,5,5,5,5,5,5,5,5,
    30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,
    20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20
]

# เพิ่ม i5 ให้แต่ละแถว
for idx, row in enumerate(rows):
    if idx < len(i5_values):
        row["i5"] = i5_values[idx]
    else:
        # ถ้ามีค่า i5 มากกว่าแถวเดิม สร้างแถวใหม่
        new_id = len(rows) + 1
        rows.append({"id": new_id, "i1":0, "i2":0, "i3":0, "i4":0, "i5": i5_values[idx]})

# บันทึกไฟล์ใหม่
with open("pattern.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
