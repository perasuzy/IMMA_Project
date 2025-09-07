import tkinter as tk
from tkinter import messagebox
import json
import uuid

def submit_orders():
    try:
        with open("orders.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            results = [rec for rec in data if rec.get("Status") == "Inprogress"]
            # print("\n","="*200,"\n",type(results),"\n","="*200,"\n")
            orders = [0,0,0]                                                                    #index 0,1,2 คือ sofas,tables,chairs
            for result in results:
                # print(result["Table"],end="\n")
                orders[0] += int(result["Sofa"])
                orders[1] += int(result["Table"])
                orders[2] += int(result["Chair"])
            total_wood_for_use = calculate_order(orders)
            for rec in data:
                rec["Status"] = "Done"
            with open("orders.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                # print("Updated all Status to Done")
            return total_wood_for_use
    except FileNotFoundError:
        print("❌ ไม่พบไฟล์ orders.json")
    except json.JSONDecodeError:
        print("⚠️ orders.json ไม่ใช่ไฟล์ JSON ที่ถูกต้อง")

def calculate_order(orders):
    total_sofa = orders[0]
    total_table = orders[1]
    total_chair = orders[2]
    
    ########################################################################################################################################################################
    # ไปเขียน function calculate เอง!!!!! เตรียมดึงจำนวนให้หมดแล้ว
    # print("sofa: ",total_sofa,"\ntable: ",total_table,"\nchair: ",total_chair,"\n")



    sum = orders[0]+orders[1]+orders[2]
    ########################################################################################################################################################################
    return sum

print("total woods : ",submit_orders())