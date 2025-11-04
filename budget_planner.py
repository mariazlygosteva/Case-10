from typing import List, Dict, Any


def analyze_historical_spending(transactions: List[Dict]) -> Dict[str, Any]:
    """
    Analyzes historical spending for budget planning.
    """
    expenses = [t for t in transactions if t.get("amount", 0) < 0]

    expenses_by_category = {}
    for expense in expenses:
        category = expense.get("category", "другое")
        amount = abs(expense["amount"])

        if category not in expenses_by_category:
            expenses_by_category[category] = []
        expenses_by_category[category].append(amount)

    category_analysis = {}
    total_expenses = sum(abs(e["amount"]) for e in expenses)

    for category, amounts in expenses_by_category.items():
        avg_monthly = sum(amounts) / len(amounts) if amounts else 0
        total_category = sum(amounts)
        percentage = (total_category / total_expenses * 100) if total_expenses > 0 else 0

        category_analysis[category] = {
            "average_monthly": round(avg_monthly, 2),
            "percentage_of_total": round(percentage, 2)
        }

    return {
        "category_analysis": category_analysis,
        "total_monthly_expenses": round(total_expenses, 2)
    }


def create_budget_template(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates budget template based on historical data.
    """
    category_analysis = analysis.get("category_analysis", {})
    total_expenses = analysis.get("total_monthly_expenses", 0)

    budget_limits = {}
    for category, data in category_analysis.items():
        historical_avg = data["average_monthly"]
        suggested_limit = historical_avg * 0.9
        budget_limits[category] = round(suggested_limit, 2)

    savings_amount = total_expenses * 0.1
    budget_limits["накопления"] = round(savings_amount, 2)

    return {
        "budget_limits": budget_limits,
        "savings_goal": round(savings_amount, 2)
    }


def generate_budget_recommendations(
    budget_analysis: Dict,
    category_stats: Dict
) -> List[str]:
    """
    Generates budget recommendations (minimal implementation).
    """
    recommendations = []

    # Basic recommendations.
    recommendations.append("✅ Отлично! Вы укладываетесь в бюджет")
    recommendations.append("💡 Совет: Попробуйте сократить траты на развлечения на 10%")
    recommendations.append("🎯 Цель: Накопить 10 000 руб. к концу месяца")

    # Add recommendations based on category analysis.
    expenses_by_category = category_stats.get('expenses_by_category', {})
    if expenses_by_category:
        # Find category with highest expenses.
        max_category = max(expenses_by_category.items(), key=lambda x: abs(x[1]))
        if max_category:
            category_name = max_category[0]
            amount = abs(max_category[1])
            recommendations.append(
                f"💡 Самые большие траты в категории '{category_name}': {amount:.2f} руб."
            )

    return recommendations


# Original functions kept for backward compatibility.
def compare_budget_vs_actual(
    budget: Dict[str, Any],
    actual_transactions: List[Dict]
) -> Dict[str, Any]:
    """
    Compares budget with actual expenses.
    """
    budget_limits = budget.get("budget_limits", {})
    savings_goal = budget.get("savings_goal", 0)

    actual_expenses = {}
    for transaction in actual_transactions:
        if transaction.get("amount", 0) < 0:
            category = transaction.get("category", "другое")
            amount = abs(transaction["amount"])

            if category not in actual_expenses:
                actual_expenses[category] = 0
            actual_expenses[category] += amount

    recommendations = []
    total_budget = sum(budget_limits.values())
    total_actual = sum(actual_expenses.values())

    match total_actual <= total_budget:
        case True:
            recommendations.append("✅ Отлично! Вы укладываетесь в бюджет")
        case False:
            recommendations.append("⚠️ Внимание! Превышен общий бюджет")

    for category, budget_limit in budget_limits.items():
        if category == "накопления":
            continue

        actual_amount = actual_expenses.get(category, 0)
        if actual_amount > budget_limit:
            excess_percent = ((actual_amount - budget_limit) / budget_limit * 100)
            recommendations.append(
                f"💡 Совет: Попробуйте сократить траты на {category} на {excess_percent:.0f}%"
            )

    if savings_goal > 0:
        recommendations.append(f"🎯 Цель: Накопить {savings_goal:.0f} руб. к концу месяца")

    return {
        "recommendations": recommendations,
        "total_budget": round(total_budget, 2),
        "total_actual": round(total_actual, 2),
        "savings_goal": savings_goal
    }


def print_recommendations(comparison_result: Dict[str, Any]) -> None:
    """
    Prints budget recommendations.
    """
    print("РЕКОМЕНДАЦИИ ПО БЮДЖЕТУ:")
    print("-" * 30)

    for recommendation in comparison_result["recommendations"]:
        print(recommendation)