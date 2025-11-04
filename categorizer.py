import re
from typing import Dict, List


def create_categories() -> Dict[str, List[str]]:
    """
    Creates extended categories dictionary with keywords.
    Includes categories for income and expenses.
    """
    categories = {
        # Expense categories.
        "еда": [
            "пятерочка", "магнит", "перекресток", "ашан", "лента", "продукты",
            "еда", "продуктовый", "супермаркет", "овощи", "фрукты", "молоко",
            "хлеб", "мясо", "рыба", "курочка", "гастроном", "бакалея", "спар"
        ],
        "транспорт": [
            "метро", "автобус", "такси", "бензин", "заправка", "транспорт",
            "проезд", "каршеринг", "яндекс.такси", "uber", "ситимобил",
            "транспортная карта", "парковка", "штраф гибдд"
        ],
        "развлечения": [
            "кино", "ресторан", "кафе", "концерт", "бар", "паб", "клуб",
            "билет", "игра", "хобби", "развлечения", "театр", "выставка",
            "музей", "боулинг", "караоке", "кофейня", "стейкхаус", "суши"
        ],
        "здоровье": [
            "аптека", "врач", "больница", "лекарства", "медицина", "стоматолог",
            "поликлиника", "анализы", "медцентр", "витамины", "спортзал", "фитнес"
        ],
        "коммуналка": [
            "квартплата", "электричество", "вода", "газ", "интернет", "телефон",
            "связь", "жкх", "коммунальные", "аренда", "ипотека", "рко", "домофон"
        ],
        "одежда": [
            "одежда", "обувь", "магазин", "бутик", "шопинг", "бренд", "zara",
            "hm", "резерв", "ламиния", "обувной", "ателье", "трикотаж"
        ],
        "образование": [
            "курсы", "учеба", "образование", "книги", "учебник", "репетитор",
            "школа", "университет", "онлайн-курс", "литература", "канцелярия"
        ],
        "техника": [
            "техника", "электроника", "смартфон", "ноутбук", "компьютер",
            "телевизор", "dns", "м.видео", "ситилинк", "гаджет", "аксессуар"
        ],
        "красота": [
            "парикмахер", "салон", "косметика", "косметолог", "маникюр",
            "стрижка", "spa", "уход", "парфюмерия", "рив гош", "лендри"
        ],

        # Income categories.
        "зарплата": [
            "зарплата", "оклад", "аванс", "заработная", "зп", "payroll",
            "начисление зп", "расчетный счет"
        ],
        "премия": [
            "премия", "бонус", "поощрение", "вознаграждение", "kpi"
        ],
        "инвестиции": [
            "дивиденды", "проценты", "инвестиции", "вклад", "депозит",
            "акции", "облигации", "купон", "инвест"
        ],
        "подарки": [
            "подарок", "сюрприз", "поздравление", "перевод", "от друга"
        ],
        "фриланс": [
            "фриланс", "проект", "удаленная работа", "заказ", "исполнение"
        ]
    }
    return categories


def categorize_transaction(
        description: str,
        amount: float,
        categories: Dict[str, List[str]]
) -> str:
    """
    Enhanced transaction categorization function.
    Uses extended keyword search.
    """
    desc_lower = description.lower()

    # Remove extra characters for improved search.
    desc_clean = re.sub(r'[^\w\s]', ' ', desc_lower)

    match amount >= 0:
        case True:
            income_categories = ["зарплата", "премия", "инвестиции", "подарки", "фриланс"]
            for category in income_categories:
                if category in categories:
                    for keyword in categories[category]:
                        if keyword in desc_lower or keyword in desc_clean:
                            return category
            return "прочие доходы"

        case False:
            expense_categories = [
                cat for cat in categories.keys()
                if cat not in ["зарплата", "премия", "инвестиции", "подарки", "фриланс"]
            ]

            # First search for exact matches.
            for category in expense_categories:
                for keyword in categories[category]:
                    if (keyword in desc_lower or
                            keyword in desc_clean or
                            any(word in desc_lower for word in keyword.split()) or
                            any(word in desc_clean for word in keyword.split())):
                        return category

            # If no exact matches, use extended search.
            for category in expense_categories:
                for keyword in categories[category]:
                    # Search by word parts.
                    keyword_parts = keyword.split()
                    if len(keyword_parts) > 1:
                        if all(part in desc_lower for part in keyword_parts):
                            return category

            return "другое"


def categorize_all_transactions(transactions: List[dict]) -> List[dict]:
    """
    Main function for categorizing all transactions.
    """
    categories = create_categories()
    categorized_transactions = []

    for transaction in transactions:
        categorized_transaction = transaction.copy()

        description = categorized_transaction.get('description', '')
        amount = categorized_transaction.get('amount', 0)

        category = categorize_transaction(description, amount, categories)
        categorized_transaction['category'] = category

        categorized_transactions.append(categorized_transaction)

    print(f"✅ Categorized {len(categorized_transactions)} transactions")
    return categorized_transactions


def get_category_summary(transactions: List[dict]) -> Dict[str, dict]:
    """
    Creates category summary for analytics.
    """
    summary = {}

    for transaction in transactions:
        category = transaction.get('category', 'не определена')
        amount = transaction.get('amount', 0)

        if category not in summary:
            summary[category] = {
                'count': 0,
                'total_amount': 0,
                'transactions': []
            }

        summary[category]['count'] += 1
        summary[category]['total_amount'] += amount
        summary[category]['transactions'].append(transaction)

    return summary


def print_categorization_report(transactions: List[dict]) -> None:
    """
    Prints categorization report.
    """
    summary = get_category_summary(transactions)

    print("\n📊 CATEGORIZATION REPORT")
    print("=" * 50)

    # Income.
    income_cats = {k: v for k, v in summary.items() if v['total_amount'] >= 0}
    if income_cats:
        print("\n📈 INCOME:")
        for category, data in income_cats.items():
            count = data['count']
            total = data['total_amount']
            print(f"  {category}: {count} transactions, amount: {total:+.2f} руб.")

    # Expenses.
    expense_cats = {k: v for k, v in summary.items() if v['total_amount'] < 0}
    if expense_cats:
        print("\n📉 EXPENSES:")
        for category, data in expense_cats.items():
            count = data['count']
            total = data['total_amount']
            print(f"  {category}: {count} transactions, amount: {total:+.2f} руб.")

    # Statistics.
    total_transactions = len(transactions)
    categorized = len([t for t in transactions if t.get('category') != 'другое'])
    categorization_rate = (
        (categorized / total_transactions) * 100
        if total_transactions > 0
        else 0
    )

    print(f"\n📈 Categorization statistics:")
    print(f"   Total transactions: {total_transactions}")
    print(f"   Successfully categorized: {categorized} ({categorization_rate:.1f}%)")
    print(f"   Not recognized: {total_transactions - categorized}")


def improve_categories(custom_categories: Dict[str, List[str]]) -> None:
    """
    Function for improving categorization with custom rules.
    """
    # This function can be extended for system learning.
    pass


# For module testing.
if __name__ == "__main__":
    # Test data.
    test_data = [
        {
            "date": "2024-01-15",
            "amount": -1500.50,
            "description": "Продукты в Пятерочке",
            "type": "расход"
        },
        {
            "date": "2024-01-10",
            "amount": 50000.00,
            "description": "Зарплата за январь",
            "type": "доход"
        },
        {
            "date": "2024-01-12",
            "amount": -350.00,
            "description": "Такси Яндекс",
            "type": "расход"
        }
    ]

    categorized = categorize_all_transactions(test_data)
    print_categorization_report(categorized)