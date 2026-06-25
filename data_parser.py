import csv

def parse_data_cabang_real(file_path="data_cabang_xyz.csv"):
    """
    Reads the semicolon-structured data_cabang_xyz.csv file,
    extracts specific detail data for the month of JUN, and cleans it up.
    """
    dealers_clean = []
    dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
    
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        
        for row in reader:
            if not row or len(row) < 3:
                continue
            
            # Check if column index 1 is the month 'JUN' and column index 2 is numerical sales data (not total text)
            if row[1].strip().upper() == "JUN" and row[2].strip().isdigit():
                # In the original file, because of leading semicolons, 'TOTAL SALES DEALER A' starts at index 2
                idx = 2 
                
                for name in dealer_names:
                    try:
                        total_sales = int(row[idx].strip()) if row[idx].strip() else 0
                        contribution = int(row[idx+1].strip()) if row[idx+1].strip() else 0
                        
                        # Clean Indonesian decimal format (e.g., 0,51% -> 0.51)
                        npl_str = row[idx+2].strip().replace("%", "").replace(",", ".")
                        npl = float(npl_str) if npl_str else 0.0
                        
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

if __name__ == "__main__":
    data = parse_data_cabang_real()
    print("=== CHECK DATA PARSING ===")
    for d in data:
        print(d)