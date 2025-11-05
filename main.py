# Case-study #10
# Developers: Sedelnikova P., Simonov A., Fedotova M.
#
"""
Main module of the financial assistant.
Combines all components of the accounting and analytics system.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import our modules.
from data_importer import import_financial_data, generate_sample_data
from categorizer import categorize_all_transactions, print_categorization_report
from analyzer import (calculate_basic_stats, calculate_by_category,
                     generate_analytics_report)
from budget_planner import (analyze_historical_spending,
                           create_budget_template, generate_budget_recommendations)
import local as ru

# Global variables for state management.
transactions = []
categorized_transactions = []
stats = {}
category_stats = {}
budget_analysis = {}
budget_template = {}


def initialize_app(language: str = "ru") -> None:
    """Initializes the application."""
    ru.set_language(language)
    print('🤑 Добро пожаловать в Финансовый Помощник!')


def load_data(filename: str = None, use_sample: bool = False) -> bool:
    """
    Loads data from file or generates sample data.

    Args:
        filename: Path to data file
        use_sample: Whether to use sample data

    Returns:
        bool: True if data loaded successfully
    """
    global transactions

    if use_sample:
        print("🎯 Генерация тестовых данных...")
        transactions = generate_sample_data()
        print('✅ Сгенерировано {} тестовых транзакций'.format(len(transactions)))
        return True

    if filename and os.path.exists(filename):
        print('📁 Импорт данных из файла: {}'.format(filename))
        transactions = import_financial_data(filename)
        if transactions:
            print('✅ Успешно импортировано {} транзакций'.format(len(transactions)))
            return True
        else:
            print('❌ Ошибка импорта данных')
            return False
    else:
        print('❌ Файл не найден')
        return False


def process_data() -> None:
    """Processes data: categorization, analysis, planning."""
    global categorized_transactions, stats, category_stats, budget_analysis,\
        budget_template

    if not transactions:
        print('❌ Нет данных для обработки')
        return

    # Step 1: Transaction categorization.
    print("\n" + "=" * 50)
    print('🏷️  КАТЕГОРИЗАЦИЯ ТРАНЗАКЦИЙ')
    print("=" * 50)
    categorized_transactions = categorize_all_transactions(transactions)

    # Step 2: Basic analysis.
    print("\n" + "=" * 50)
    print('📊 АНАЛИЗ ФИНАНСОВЫХ ДАННЫХ')
    print("=" * 50)
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)

    # Step 3: Budget planning.
    print("\n" + "=" * 50)
    print('🎯 ПЛАНИРОВАНИЕ БЮДЖЕТА')
    print("=" * 50)
    budget_analysis = analyze_historical_spending(categorized_transactions)
    budget_template = create_budget_template(budget_analysis)


def get_category_emoji(category: str) -> str:
    """
    Returns emoji for category.

    Args:
        category: Category name

    Returns:
        str: Emoji for the category
    """
    emoji_map = {
        'еда': '🍎',
        'транспорт': '🚗',
        'развлечения': '🎭',
        'здоровье': '🏥',
        'коммуналка': '🏠',
        'одежда': '👕',
        'образование': '📚',
        'техника': '💻',
        'красота': '💄',
        'зарплата': '💰',
        'премия': '🎁',
        'инвестиции': '📈',
        'подарки': '🎁',
        'фриланс': '💼',
        'другое': '📦',
        'прочие доходы': '💵'
    }
    return emoji_map.get(category, '📌')


def print_basic_stats() -> None:
    """Prints basic financial indicators."""
    print(f"\n{ru.TEXTS_RU['basic_stats']}:")
    print("-" * 40)

    income = stats.get('total_income', 0)
    expenses = stats.get('total_expenses', 0)
    balance = stats.get('balance', 0)

    print(f"💰 {ru.TEXTS_RU['total_income']}: {ru.format_currency(income)}")
    print(f"💸 {ru.TEXTS_RU['total_expenses']}: {ru.format_currency(expenses)}")
    print(f"⚖️  {ru.TEXTS_RU['balance']}: {ru.format_currency(balance)}")

    if income > 0:
        savings_rate = (balance / income) * 100
        print(f"🎯 {ru.TEXTS_RU['savings_rate']}: {savings_rate:.1f}%")

        if savings_rate >= 20:
            print("   ✅ Отличный уровень сбережений!")
        elif savings_rate >= 10:
            print("   ⚠️  Хорошо, но можно лучше")
        else:
            print("   💡 Рекомендуем увеличить сбережения")


def print_category_analysis() -> None:
    """Prints analysis by categories."""
    print(f"\n{ru.TEXTS_RU['category_analysis']}:")
    print("-" * 40)

    expenses_by_category = category_stats.get('expenses_by_category', {})
    total_expenses = stats.get('total_expenses', 1)

    if not expenses_by_category:
        print(ru.TEXTS_RU['no_expense_data'])
        return

    sorted_categories = sorted(
        expenses_by_category.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    for category, amount in sorted_categories:
        percentage = (abs(amount) / total_expenses) * 100
        emoji = get_category_emoji(category)
        print(f"  {emoji} {category}: {ru.format_currency(abs(amount))} ("
              f"{percentage:.1f}%)")


def print_budget_recommendations() -> None:
    """Prints budget recommendations."""
    print(f"\n{ru.TEXTS_RU['budget_recommendations']}:")
    print("-" * 40)

    recommendations = generate_budget_recommendations(
        budget_analysis, category_stats)

    for rec in recommendations:
        print(f"  {rec}")


def print_additional_insights() -> None:
    """Prints additional analytics insights."""
    print(f"\n{ru.TEXTS_RU['additional_insights']}:")
    print("-" * 40)

    large_expenses = stats.get('largest_expenses', [])
    if large_expenses:
        print(f"\n📊 {ru.TEXTS_RU['largest_expenses']}:")
        for expense in large_expenses[:3]:
            desc = expense.get('description', 'No description')
            amount = expense.get('amount', 0)
            print(f"   • {desc}: {ru.format_currency(abs(amount))}")

    monthly_stats = stats.get('monthly_stats', {})
    if monthly_stats:
        print(f"\n📈 {ru.TEXTS_RU['monthly_trends']}:")
        for month, data in list(monthly_stats.items())[-3:]:
            balance = data.get('balance', 0)
            print(f"   • {month}: {ru.format_currency(balance)}")


def generate_report() -> None:
    """Generates complete financial report."""
    if not categorized_transactions:
        print(ru.TEXTS_RU["no_processed_data"])
        return

    print("\n" + "=" * 60)
    print(ru.TEXTS_RU["report_title"])
    print("=" * 60)

    print_basic_stats()
    print_category_analysis()
    print_budget_recommendations()
    print_additional_insights()


def save_results(filename: str = None) -> None:
    """
    Saves analysis results to file.

    Args:
        filename: Output filename
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"financial_report_{timestamp}.txt"

    # Check if we can write to the file.
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Open file for writing.
    file_obj = open(filename, 'w', encoding='utf-8')

    # Save main report.
    file_obj.write("FINANCIAL REPORT\n")
    file_obj.write("=" * 50 + "\n\n")

    # Main indicators.
    file_obj.write("MAIN INDICATORS:\n")
    file_obj.write(f"Income: {ru.format_currency(stats.get('total_income', 0))}\n")
    file_obj.write(f"Expenses: {ru.format_currency(stats.get(
        'total_expenses', 0))}\n")
    file_obj.write(f"Balance: {ru.format_currency(stats.get('balance', 0))}\n\n")

    # Expense categories.
    file_obj.write("EXPENSES BY CATEGORY:\n")
    expenses_by_category = category_stats.get('expenses_by_category', {})
    total_expenses = stats.get('total_expenses', 1)

    for category, amount in expenses_by_category.items():
        percentage = (abs(amount) / total_expenses) * 100
        file_obj.write(f"{category}: {ru.format_currency(abs(amount))} ("
                       f"{percentage:.1f}%)\n")

    file_obj.write(f"\nReport saved: {datetime.now().strftime(
        '%Y-%m-%d %H:%M')}\n")
    file_obj.close()

    print(ru.TEXTS_RU['report_saved'].format(filename))


def show_menu() -> None:
    """Displays main menu."""
    print("\n" + "=" * 50)
    print('ГЛАВНОЕ МЕНЮ')
    print("=" * 50)
    print("1. 📁 Загрузить данные из файла")
    print("2. 🎯 Сгенерировать тестовые данные")
    print("3. 📊 Сгенерировать полный отчет")
    print("4. 💾 Сохранить отчет в файл")
    print("5. 🔍 Показать детальную аналитику")
    print("6. 🚪 Выход")
    print("=" * 50)


def main() -> None:
    """Main program function."""
    initialize_app()

    while True:
        show_menu()
        choice = input("\nSelect action (1-6): ").strip()

        match choice:
            case "1":
                filename = input("Enter filename (CSV or JSON): ").strip()
                load_data(filename)
                if transactions:
                    process_data()

            case "2":
                load_data(use_sample=True)
                process_data()

            case "3":
                if categorized_transactions:
                    generate_report()
                else:
                    print("❌ Please load data first!")

            case "4":
                if categorized_transactions:
                    filename = input(
                        "Enter filename for saving (or press Enter for auto-name): "
                    ).strip()
                    if not filename:
                        filename = None
                    save_results(filename)
                else:
                    print("❌ No data to save!")

            case "5":
                if categorized_transactions:
                    print("\n" + "=" * 50)
                    print("DETAILED ANALYTICS")
                    print("=" * 50)
                    print_categorization_report(categorized_transactions)
                    generate_analytics_report(stats, category_stats)
                else:
                    print("❌ Please load data first!")

            case "6":
                print(ru.TEXTS_RU["goodbye"])
                break

            case _:
                print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
