from typing import Dict, List, Any


def calculate_basic_stats(transactions: list) -> dict:
    """
    Calculates basic financial indicators.
    """
    income = 0
    expenses = 0
    largest_expenses = []

    for transaction in transactions:
        amount = transaction["amount"]
        if amount >= 0:
            income += amount
        else:
            expenses += amount
            # Track largest expenses
            largest_expenses.append(transaction)

    balance = income + expenses

    # Sort largest expenses
    largest_expenses.sort(key=lambda x: x["amount"])

    # Get monthly stats
    monthly_stats = {}
    for transaction in transactions:
        date_str = transaction["date"]
        if len(date_str) >= 7:  # At least YYYY-MM
            month_key = date_str[:7]  # YYYY-MM
            if month_key not in monthly_stats:
                monthly_stats[month_key] = {"income": 0, "expenses": 0, "balance": 0}

            if transaction["amount"] >= 0:
                monthly_stats[month_key]["income"] += transaction["amount"]
            else:
                monthly_stats[month_key]["expenses"] += transaction["amount"]

            monthly_stats[month_key]["balance"] = monthly_stats[month_key]["income"] + monthly_stats[month_key][
                "expenses"]

    return {
        "total_income": income,
        "total_expenses": abs(expenses),  # Positive number for expenses
        "balance": balance,
        "transaction_count": len(transactions),
        "largest_expenses": largest_expenses[:5],  # Top 5 largest expenses
        "monthly_stats": monthly_stats
    }


def calculate_by_category(transactions: list) -> dict:
    """
    Analyzes expenses by categories.
    """
    expenses_by_category = {}
    income_by_category = {}

    for transaction in transactions:
        category = transaction.get("category", "другое")
        amount = transaction["amount"]

        if amount < 0:  # Expense
            if category not in expenses_by_category:
                expenses_by_category[category] = 0
            expenses_by_category[category] += amount
        else:  # Income
            if category not in income_by_category:
                income_by_category[category] = 0
            income_by_category[category] += amount

    return {
        "expenses_by_category": expenses_by_category,
        "income_by_category": income_by_category
    }


def generate_analytics_report(stats: Dict, category_stats: Dict) -> None:
    """
    Generates analytics report.
    """
    print("\n📈 ADDITIONAL ANALYTICS")
    print("=" * 40)
    print(f"Total transactions: {stats.get('transaction_count', 0)}")

    expenses_by_category = category_stats.get('expenses_by_category', {})
    if expenses_by_category:
        print("\n📊 EXPENSE DETAILS BY CATEGORY:")
        for category, amount in expenses_by_category.items():
            print(f"  {category}: {abs(amount):.2f} руб.")


# Keep original functions under different names for backward compatibility
def _calculate_basic_stats_original(transactions: list) -> dict:
    """Original version of the function."""
    income = 0
    expenses = 0

    for transaction in transactions:
        if transaction.get("type") == "доход":
            income += transaction["amount"]
        elif transaction.get("type") == "расход":
            expenses += transaction["amount"]

    balance = income + expenses

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "transactions_n": len(transactions)
    }


def _calculate_by_category_original(transactions: list) -> dict:
    """Original version of the function."""
    basic_stats = _calculate_basic_stats_original(transactions)
    expenses = basic_stats["expenses"]
    category_totals = {}

    # Create list of categories from transactions
    categories = set()
    for transaction in transactions:
        if "category" in transaction:
            categories.add(transaction["category"])

    for category in categories:
        category_statistics = {}
        category_transactions = []

        for transaction in transactions:
            if transaction.get("category") == category:
                category_transactions.append(transaction)

        if not category_transactions:
            continue

        stats = _calculate_basic_stats_original(category_transactions)

        category_statistics["total_sum"] = stats["balance"]
        category_statistics["transactions_n"] = stats["transactions_n"]
        if expenses != 0:
            category_statistics["percent_of_expenses"] = (
                    abs(stats["expenses"]) / abs(expenses) * 100
            )
        else:
            category_statistics["percent_of_expenses"] = 0

        category_totals[category] = category_statistics

    return category_totals