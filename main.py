from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

# -----------------------------
# Step 1: Read & Parse Data
# -----------------------------
file_path = "data/sales_data.txt"
raw_lines = read_sales_data(file_path)
transactions = parse_transactions(raw_lines)

# -----------------------------
# Step 2: Validate & Filter
# (Handles Question 2 summary internally)
# -----------------------------
valid_transactions, invalid_count, summary = validate_and_filter(transactions)

# -----------------------------
# Step 3: Print Summary (Q2)
# -----------------------------
print("\n--- DATA VALIDATION SUMMARY ---")
print("Invalid records:", invalid_count)
print("Summary:", summary)

# -----------------------------
# Step 4: Sales Analytics (Q3)
# -----------------------------
print("\n--- SALES ANALYTICS ---")
print("Total Revenue:", calculate_total_revenue(valid_transactions))
print("Region-wise Sales:", region_wise_sales(valid_transactions))
print("Top Selling Products:", top_selling_products(valid_transactions))

# -----------------------------
# Step 5: Customer Analysis
# -----------------------------
print("\n--- CUSTOMER ANALYSIS ---")
print("Customer Analysis:", customer_analysis(valid_transactions))

# -----------------------------
# Step 6: Time-based Analysis
# -----------
print("\n========== DAILY SALES TREND ==========")
trend = daily_sales_trend(valid_transactions)
for date, info in trend.items():
    print(date, "->", info)

print("\n========== PERFORMANCE INSIGHTS ==========")
peak = find_peak_sales_day(valid_transactions)
print("Peak Sales Day:", peak)

low_products = low_performing_products(valid_transactions)
print("Low Performing Products:")
for product in low_products:
    print(product)

with open("output/sales_report.txt", "w") as report:
    report.write("SALES ANALYTICS REPORT\n")
    report.write("=" * 30 + "\n\n")

    report.write(f"Total Revenue: {calculate_total_revenue(valid_transactions)}\n\n")

    report.write("Region-wise Sales:\n")
    for region, data in region_wise_sales(valid_transactions).items():
        report.write(f"{region}: {data}\n")

    report.write("\nTop Selling Products:\n")
    for product in top_selling_products(valid_transactions):
        report.write(f"{product}\n")

    peak_day = find_peak_sales_day(valid_transactions)
    report.write(f"\nPeak Sales Day: {peak_day}\n")

    report.write("\nLow Performing Products:\n")
    for product in low_performing_products(valid_transactions):
        report.write(f"{product}\n")

with open("output/enriched_sales_data.txt", "w") as enriched:
    enriched.write("transaction,revenue\n")

    for tx in valid_transactions:
        # Extract all numeric values from transaction
        numeric_values = [v for v in tx.values() if isinstance(v, (int, float))]

        if len(numeric_values) >= 2:
            quantity = numeric_values[-2]
            price = numeric_values[-1]
            revenue = quantity * price
        else:
            revenue = 0

        enriched.write(f"{tx},{revenue}\n")

