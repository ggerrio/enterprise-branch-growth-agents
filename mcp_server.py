import csv
import json
import os

class VesselBankDataServer:
    def __init__(self, db_path="Dealer_Sales_and_NPL.csv"):
        self.db_path = db_path
        self._ensure_mock_db()

    def _ensure_mock_db(self):
        """Ensures that the mock Vessel Bank branch data is available if it doesn't exist yet."""
        if not os.path.exists(self.db_path):
            headers = ["Showroom_Name", "Booking_Volume_Last_Month", "Booking_Volume_This_Month", "NPL_Percent", "CMO_Handler_Name"]
            data = [
                ["Showroom_Garuda_Motor", "50", "35", "1.2", "Budi_Santoso"],
                ["Showroom_Maju_Jaya", "30", "28", "0.8", "Siti_Aminah"],
                ["Showroom_Raya_Automobil", "40", "20", "3.5", "Iwan_Setiawan"],
                ["Showroom_Berkat_Mobilindo", "25", "24", "1.5", "Budi_Santoso"],
                ["Showroom_Tunas_Harapan", "15", "5", "4.2", "Siti_Aminah"]
            ]
            with open(self.db_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data)

    def fetch_branch_records(self) -> str:
        """Core MCP function to read internal branch database."""
        try:
            with open(self.db_path, "r") as file:
                reader = csv.DictReader(file)
                return json.dumps([row for row in reader], indent=2)
        except Exception as e:
            return f"Error reading MCP database: {str(e)}"