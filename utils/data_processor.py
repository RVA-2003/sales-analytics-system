def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip incorrect rows
        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0]
            date = parts[1]
            product_id = parts[2]

            # Handle commas in product name
            product_name = parts[3].replace(",", "")

            # Remove commas from numbers
            quantity = int(parts[4].replace(",", ""))
            unit_price = float(parts[5].replace(",", ""))

            customer_id = parts[6]
            region = parts[7]

            transaction = {
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    for tx in transactions:
        try:
            if not tx["Region"]:
               invalid_count += 1
               continue

            if tx["Quantity"] <= 0:
                invalid_count += 1
                continue

            if tx["UnitPrice"] <= 0:
                invalid_count += 1
                continue

            if not tx["TransactionID"].startswith("T"):
                invalid_count += 1
                continue

            if not tx["ProductID"].startswith("P"):
                invalid_count += 1
                continue

            if not tx["CustomerID"].startswith("C"):
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    # Display available regions
    regions = set(tx["Region"] for tx in valid_transactions)
    print("Available Regions:", regions)

    filtered = valid_transactions

    if region:
        filtered = [tx for tx in filtered if tx["Region"] == region]

    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in filtered]
    if amounts:
        print("Transaction Amount Range:", min(amounts), "-", max(amounts))

    if min_amount:
        filtered = [tx for tx in filtered if tx["Quantity"] * tx["UnitPrice"] >= min_amount]

    if max_amount:
        filtered = [tx for tx in filtered if tx["Quantity"] * tx["UnitPrice"] <= max_amount]

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": len(filtered) if region else 0,
        "filtered_by_amount": len(filtered) if min_amount or max_amount else 0,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return total_revenue
def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Calculate percentage
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )

    return sorted_regions
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = {}

    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = quantity * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    # Convert to list of tuples
    product_list = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
    ]

    # Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    return product_list[:n]
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = {}

    for tx in transactions:
        customer = tx["CustomerID"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customer_data[customer]["total_spent"] += revenue
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products"].add(product)

    # Prepare final output
    result = {}

    for customer, data in customer_data.items():
        result[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": list(data["products"])
        }

    # Sort by total_spent descending
    sorted_result = dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )

    return sorted_result
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Format output
    result = {}

    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """

    daily_data = {}

    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']

        if date not in daily_data:
            daily_data[date] = {'revenue': 0, 'count': 0}

        daily_data[date]['revenue'] += revenue
        daily_data[date]['count'] += 1

    peak_date = None
    peak_revenue = 0
    peak_count = 0

    for date, data in daily_data.items():
        if data['revenue'] > peak_revenue:
            peak_revenue = data['revenue']
            peak_date = date
            peak_count = data['count']

    return (peak_date, round(peak_revenue, 2), peak_count)
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    for t in transactions:
        product = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if product not in product_data:
            product_data[product] = {'qty': 0, 'revenue': 0}

        product_data[product]['qty'] += qty
        product_data[product]['revenue'] += revenue

    low_products = []

    for product, data in product_data.items():
        if data['qty'] < threshold:
            low_products.append(
                (product, data['qty'], round(data['revenue'], 2))
            )

    # Sort by quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

