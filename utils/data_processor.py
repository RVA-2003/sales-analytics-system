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

