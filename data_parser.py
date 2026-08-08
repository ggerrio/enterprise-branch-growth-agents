from branch_growth_analyst.data_parser import (
    parse_indonesian_number,
    parse_indonesian_percent,
    format_indonesian_number,
    format_indonesian_percent,
    parse_data_cabang_real,
    parse_june_data,
)

if __name__ == "__main__":
    data = parse_data_cabang_real()
    print("=== CHECK DATA PARSING ===")
    for d in data:
        print(d)