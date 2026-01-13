from utils.api_handler import get_sales_summary

file_path = "data/sales_data.txt"

result = get_sales_summary(file_path)

print("\n--- SALES ANALYSIS ---")
print(f"Total Revenue: ₹{result['total_revenue']:,.2f}")

print("\nSales by Region:")
for region, revenue in result["sales_by_region"].items():
    print(f"{region}: ₹{revenue:,.2f}")

print(f"\nTop Selling Product: {result['top_product']}")

