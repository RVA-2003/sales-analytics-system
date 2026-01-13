from utils.file_handler import clean_sales_data
from utils.data_processor import analyze_sales_data


def get_sales_summary(file_path):
    cleaned_data = clean_sales_data(file_path)
    analysis_result = analyze_sales_data(cleaned_data)
    return analysis_result
