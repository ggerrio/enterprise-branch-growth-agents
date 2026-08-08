import csv
import os

def parse_indonesian_number(val_str):
    if not val_str:
        return 0
    cleaned = str(val_str).replace(".", "").strip()
    return int(cleaned) if cleaned.isdigit() else 0

def format_indonesian_number(val_int):
    return f"{val_int:,}".replace(",", ".")

def parse_indonesian_percent(val_str):
    if not val_str:
        return 0.0
    cleaned = str(val_str).replace("%", "").replace(",", ".").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def format_indonesian_percent(val_float):
    if val_float == int(val_float):
        return f"{int(val_float)}%"
    formatted = f"{val_float:.2f}".replace(".", ",")
    return f"{formatted}%"

def parse_data_cabang_real(file_path="data_cabang_xyz.csv"):
    """
    Reads the semicolon-structured data_cabang_xyz.csv file,
    extracts specific detail data for the month of JUN, and cleans it up.
    """
    dealers_clean = []
    dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
    
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        
        for row in reader:
            if not row or len(row) < 3:
                continue
            
            # Check if column index 1 is the month 'JUN' and column index 2 is numerical sales data (not total text)
            if row[1].strip().upper() == "JUN" and row[2].strip().isdigit():
                idx = 2 
                
                for name in dealer_names:
                    try:
                        total_sales = int(row[idx].strip()) if row[idx].strip() else 0
                        contribution = int(row[idx+1].strip()) if row[idx+1].strip() else 0
                        
                        # Clean Indonesian decimal format (e.g., 0,51% -> 0.51)
                        npl = parse_indonesian_percent(row[idx+2])
                        
                        # Simulate a higher previous volume to create a drop gap
                        # Example: Dealer A contribution June = 21, we simulate May = 35 (drop of 14 units)
                        vol_last_month = contribution + 14 if contribution > 0 else 0
                        
                        cmo_assignment = "Budi_Santoso" if len(dealers_clean) % 2 == 0 else "Siti_Aminah"
                        
                        dealers_clean.append({
                            "Showroom_Name": name.replace(" ", "_"),
                            "Booking_Volume_Last_Month": vol_last_month,
                            "Booking_Volume_This_Month": contribution,
                            "NPL_Percent": npl,
                            "CMO_Handler_Name": cmo_assignment
                        })
                    except (IndexError, ValueError):
                        pass
                    idx += 3 # Jump to next dealer block (Total, Contribution, NPL)
                break # Finished reading June row
                
    return dealers_clean

def parse_june_data(file_path="data_cabang_xyz.csv"):
    """
    Reads data_cabang_xyz.csv and extracts June details dynamically.
    For simulate_committee.py backward compatibility.
    """
    dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
    dealers = []
    macro_data = {}
    
    if not os.path.exists(file_path):
        return dealers, macro_data

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = list(csv.reader(file, delimiter=";"))
        
        # 1. Parse Macro Data (Jan - Jun)
        for row in reader:
            if not row or len(row) < 5:
                continue
            month = row[1].strip()
            if month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]:
                macro_data[month] = {
                    "target": row[2].strip(),
                    "achv_pct": row[3].strip(),
                    "achv_rp": row[4].strip(),
                    "npl": row[5].strip() if len(row) > 5 else "",
                    "staff": row[6].strip() if len(row) > 6 else ""
                }
        
        # 2. Parse Contribution & NPL per Dealer (June)
        for row in reader:
            if not row or len(row) < 3:
                continue
            
            if row[1].strip().upper() == "JUN" and row[2].strip().isdigit():
                idx = 2
                for name in dealer_names:
                    try:
                        total_sales = int(row[idx].strip()) if row[idx].strip() else 0
                        kontribusi = int(row[idx+1].strip()) if row[idx+1].strip() else 0
                        npl = parse_indonesian_percent(row[idx+2])
                        
                        dealers.append({
                            "name": name,
                            "total_sales": total_sales,
                            "kontribusi": kontribusi,
                            "npl": npl
                        })
                    except (IndexError, ValueError):
                        pass
                    idx += 3
                break
                
    return dealers, macro_data
