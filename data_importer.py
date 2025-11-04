"""Module for importing financial data from CSV and JSON files."""

import json
import csv
import os
from datetime import datetime


def read_csv_file(filename: str) -> list:
    """
    Reads CSV file and converts it to a list of dictionaries.

    Args:
        filename: Path to CSV file

    Returns:
        list: List of normalized transactions
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return []

    with open(filename, 'r', encoding='utf-8') as file:
        sample = file.read(1024)
        file.seek(0)

        delimiter = ';' if ';' in sample else ','
        reader = csv.DictReader(file, delimiter=delimiter)

        return [
            normalize_csv_row(row)
            for row in reader
            if any(row.values()) and normalize_csv_row(row)
        ]


def normalize_csv_row(row: dict) -> dict:
    """
    Normalizes CSV row into standard transaction format.

    Args:
        row: Dictionary with CSV row data

    Returns:
        dict: Normalized transaction or None
    """
    row = {key.lower().strip(): value for key, value in row.items()}

    # Date processing.
    date_fields = ['date', 'дата', 'data', 'transaction_date']
    date_value = _get_first_matching_value(row, date_fields)

    if not date_value:
        return None

    normalized_date = normalize_date(date_value)
    if not normalized_date:
        return None

    # Amount processing.
    amount_fields = ['amount', 'сумма', 'sum', 'transaction_amount']
    amount_value = _get_first_matching_value(row, amount_fields)

    if not amount_value or not _is_float(amount_value):
        return None

    amount = float(amount_value.replace(',', '.').replace(' ', ''))

    # Operation type determination.
    amount = _determine_amount_sign(amount, row)

    # Description processing.
    desc_fields = ['description', 'описание', 'comment', 'назначение', 'merchant']
    description = _get_first_matching_value(row, desc_fields) or 'No description'

    return {
        'date': normalized_date,
        'amount': amount,
        'description': description,
        'type': 'income' if amount >= 0 else 'expense'
    }


def _get_first_matching_value(data_dict: dict, fields: list) -> str:
    """
    Finds first existing value from field list.

    Args:
        data_dict: Dictionary for searching
        fields: List of fields to check

    Returns:
        str: Found value or empty string
    """
    for field in fields:
        if field in data_dict and data_dict[field]:
            return str(data_dict[field])
    return ''


def _is_float(value: str) -> bool:
    """
    Checks if string can be converted to float.

    Args:
        value: String to check

    Returns:
        bool: True if can be converted to float
    """
    if not value:
        return False

    cleaned_value = value.replace(',', '.').replace(' ', '')

    # Check for only one dot and digits.
    dot_count = cleaned_value.count('.')
    numeric_chars = cleaned_value.replace('.', '').replace('-', '')

    return (dot_count <= 1 and
            numeric_chars.isdigit() and
            len(numeric_chars) > 0 and
            cleaned_value not in ['.', '-'])


def _determine_amount_sign(amount: float, row: dict) -> float:
    """
    Determines amount sign based on operation type.

    Args:
        amount: Original amount
        row: Dictionary with transaction data

    Returns:
        float: Amount with correct sign
    """
    sign_fields = ['type', 'тип', 'debit/credit']
    sign_value = _get_first_matching_value(row, sign_fields).lower()

    match sign_value:
        case sign if any(word in sign for word in ['debit', 'расход', 'списание', '-']):
            return -abs(amount)
        case sign if any(word in sign for word in ['credit', 'доход', 'пополнение', '+']):
            return abs(amount)
        case _:
            return amount


def normalize_date(date_str: str) -> str:
    """
    Normalizes date to YYYY-MM-DD format.

    Args:
        date_str: Date string

    Returns:
        str: Normalized date or original string
    """
    if not date_str:
        return date_str

    clean_date = date_str.split(' ')[0]

    date_formats = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y.%m.%d'
    ]

    for fmt in date_formats:
        if _is_valid_date(clean_date, fmt):
            date_obj = datetime.strptime(clean_date, fmt)
            return date_obj.strftime('%Y-%m-%d')

    return clean_date


def _is_valid_date(date_str: str, fmt: str) -> bool:
    """
    Checks if string matches date format.

    Args:
        date_str: Date string
        fmt: Format to check

    Returns:
        bool: True if string matches format
    """
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


def read_json_file(filename: str) -> list:
    """
    Reads JSON file and converts it to list of dictionaries.

    Args:
        filename: Path to JSON file

    Returns:
        list: List of normalized transactions
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"Error reading JSON file {filename}")
        return []

    # Ensure data is a list.
    data_list = data if isinstance(data, list) else [data]

    return [
        normalize_json_item(item)
        for item in data_list
        if normalize_json_item(item)
    ]


def normalize_json_item(item: dict) -> dict:
    """
    Normalizes JSON item into standard transaction format.

    Args:
        item: JSON item

    Returns:
        dict: Normalized transaction or None
    """
    # Date processing.
    date_fields = ['date', 'дата', 'transactionDate', 'timestamp']
    date_value = _get_first_matching_value(item, date_fields)

    if not date_value:
        return None

    normalized_date = normalize_date(date_value)
    if not normalized_date:
        return None

    # Amount processing.
    amount_fields = ['amount', 'сумма', 'sum', 'value']
    amount_value = _get_first_matching_value(item, amount_fields)

    if not amount_value or not _is_float(amount_value):
        return None

    amount = float(amount_value.replace(',', '.'))

    # Amount sign correction.
    amount = _adjust_json_amount_sign(amount, item)

    # Description processing.
    desc_fields = ['description', 'описание', 'comment', 'message', 'details']
    description = _get_first_matching_value(item, desc_fields) or 'No description'

    return {
        'date': normalized_date,
        'amount': amount,
        'description': description,
        'type': 'income' if amount >= 0 else 'expense'
    }


def _adjust_json_amount_sign(amount: float, item: dict) -> float:
    """
    Adjusts amount sign for JSON data.

    Args:
        amount: Original amount
        item: JSON item

    Returns:
        float: Amount with correct sign
    """
    if 'type' not in item:
        return amount

    trans_type = str(item['type']).lower()

    match trans_type:
        case t if any(word in t for word in ['debit', 'expense', 'расход', 'outcome']):
            return -abs(amount)
        case t if any(word in t for word in ['credit', 'income', 'доход', 'revenue']):
            return abs(amount)
        case _:
            return amount


def import_financial_data(filename: str) -> list:
    """
    Imports financial data from file.

    Args:
        filename: Path to file (CSV or JSON)

    Returns:
        list: List of valid transactions
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return []

    file_extension = filename.lower().split('.')[-1]

    match file_extension:
        case 'csv':
            raw_data = read_csv_file(filename)
        case 'json':
            raw_data = read_json_file(filename)
        case _:
            print(f"Unsupported file format: {file_extension}")
            return []

    valid_transactions = [
        transaction for transaction in raw_data
        if (transaction and
            transaction.get('date') and
            transaction.get('amount') != 0)
    ]

    print(f"Successfully imported {len(valid_transactions)} transactions from {filename}")
    return valid_transactions


def generate_sample_data() -> list:
    """
    Generates sample data for demonstration.

    Returns:
        list: List of sample transactions
    """
    return [
        {
            "date": "2024-01-15",
            "amount": -1500.50,
            "description": "Продукты в Пятерочке",
            "type": "expense"
        },
        {
            "date": "2024-01-10",
            "amount": 50000.00,
            "description": "Зарплата за январь",
            "type": "income"
        },
        {
            "date": "2024-01-12",
            "amount": -350.00,
            "description": "Такси Яндекс",
            "type": "expense"
        },
        {
            "date": "2024-01-08",
            "amount": -1200.00,
            "description": "Ресторан Суши Wok",
            "type": "expense"
        },
        {
            "date": "2024-01-20",
            "amount": 5000.00,
            "description": "Премия за проект",
            "type": "income"
        },
        {
            "date": "2024-01-05",
            "amount": -450.00,
            "description": "Аптека №1",
            "type": "expense"
        },
        {
            "date": "2024-01-18",
            "amount": -2200.00,
            "description": "Магнит косметик",
            "type": "expense"
        },
        {
            "date": "2024-01-25",
            "amount": -750.00,
            "description": "Кинотеатр Формула Кино",
            "type": "expense"
        }
    ]


if __name__ == "__main__":
    sample_data = generate_sample_data()
    print("Sample data generated successfully")