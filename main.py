from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

file_path = "data/sales_data.txt"

raw_lines = read_sales_data(file_path)
transactions = parse_transactions(raw_lines)

valid_tx, invalid_count, summary = validate_and_filter(
    transactions,
    region=None,
    min_amount=None,
    max_amount=None
)

print("Invalid records:", invalid_count)
print("Summary:", summary)


