import requests


BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API (limit=100)
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API Fetch Successful")
        return data.get("products", [])
    except Exception as e:
        print("API Fetch Failed:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """
    product_map = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is not None:
            product_map[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating"),
            }

    return product_map


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transactions with API product data
    """
    enriched = []

    for tx in transactions:
        tx_copy = tx.copy()

        product_id_raw = tx.get("product_id", "")
        numeric_id = "".join(filter(str.isdigit, product_id_raw))

        api_data = None
        if numeric_id:
            api_data = product_mapping.get(int(numeric_id))

        if api_data:
            tx_copy["API_Category"] = api_data["category"]
            tx_copy["API_Brand"] = api_data["brand"]
            tx_copy["API_Rating"] = api_data["rating"]
            tx_copy["API_Match"] = True
        else:
            tx_copy["API_Category"] = None
            tx_copy["API_Brand"] = None
            tx_copy["API_Rating"] = None
            tx_copy["API_Match"] = False

        enriched.append(tx_copy)

    return enriched


def save_enriched_data(enriched_transactions, filename="output/enriched_sales_data.txt"):
    """
    Saves enriched transactions to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = [str(tx.get(h, "")) for h in headers]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
