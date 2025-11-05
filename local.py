WELCOME = '🤑 Добро пожаловать в Финансовый Помощник!'
GENERATION = '🎯 Генерация тестовых данных...'
GENERATION_2 = '✅ Сгенерировано {} тестовых транзакций'
IMPORT = '📁 Импорт данных из файла: {}'
IMPORT_2 = '✅ Успешно импортировано {} транзакций'
ERROR = '❌ Ошибка импорта данных'
FILE = '❌ Файл не найден'
PROCESSING = '❌ Нет данных для обработки'
CATEGORIZATION = '🏷️  КАТЕГОРИЗАЦИЯ ТРАНЗАКЦИЙ'
ANALYSIS = '📊 АНАЛИЗ ФИНАНСОВЫХ ДАННЫХ'
BUDGET = '🎯 ПЛАНИРОВАНИЕ БЮДЖЕТА'
FOOD = 'еда'
TRANSPORT = 'транспорт'
FUN = 'развлечения'
HEALTH = 'здоровье'
COMMUNAL_APARTMENT = 'коммуналка'
CLOTHES = 'одежда'
EDUCATION = 'образование'
TECHNIC = 'техника'
BEAUTY = 'красота'
SALARY = 'зарплата'
PRIZE = 'премия'
INVESTMENT = 'инвестиции'
PRESENTS = 'подарки'
FREELANCE = 'фриланс'
OTHER = 'другое'
OTHERS = 'прочие доходы'
BASIC_STATS = 'ОСНОВНЫЕ ПОКАЗАТЕЛИ'
TOTAL_INCOME = 'Доходы'
TOTAL_EXPENSES = 'Расходы'
BALANCE = 'Баланс'
SAVINGS_RATE = 'Процент сбережений'
SUPER = '   ✅ Отличный уровень сбережений!'
GOOD = '   ⚠️  Хорошо, но можно лучше'
BAD = '   💡 Рекомендуем увеличить сбережения'
CATEGORY_ANALYSIS = 'РАСХОДЫ ПО КАТЕГОРИЯМ'
NO_EXPENSE_DATA = 'Нет данных о расходах'
BUDGET_RECOMMENDATION = 'РЕКОМЕНДАЦИИ ПО БЮДЖЕТУ'
ADDITIONAL_INSIGHTS = 'ДОПОЛНИТЕЛЬНАЯ АНАЛИТИКА'
LARGEST_EXPENSES = 'Самые крупные траты'
MONTHLY_TRENDS = 'Динамика по месяцам'
NO_PROCESSED_DATA = '❌ Нет обработанных данных'
REPORT_TITLE = 'ФИНАНСОВЫЙ ОТЧЕТ'
REPORT_SAVED = '✅ Отчет сохранен в файл: {}'
MENU = 'ГЛАВНОЕ МЕНЮ'
LOADING = '1. 📁 Загрузить данные из файла'
TEST = '2. 🎯 Сгенерировать тестовые данные'
REPORT = '3. 📊 Сгенерировать полный отчет'
SAVE = '4. 💾 Сохранить отчет в файл'
DETAILS = '5. 🔍 Показать детальную аналитику'
EXIT = '6. 🚪 Выход'
PLEASE = '❌ Пожалуйста, сначала загрузите данные!'
SAVES = '❌ Нет данных для сохранения!'
AGAIN = '❌ Неверный выбор! Пожалуйста, попробуйте снова.'

# Current language.
_current_language = "ru"

def set_language(language: str):
    """Set the current language for the application."""
    global _current_language
    _current_language = language

def format_currency(amount: float) -> str:
    """Format currency amount with Russian ruble symbol and proper formatting."""
    return f"{amount:,.2f} руб.".replace(',', ' ')

def format_date(date_string: str) -> str:
    """Format date from YYYY-MM-DD format to DD.MM.YYYY format."""
    # Check the basic structure of the date string.
    if (len(date_string) == 10 and
            date_string[4] == '-' and
            date_string[7] == '-'):

        parts = date_string.split('-')
        if len(parts) == 3:
            year, month, day = parts

            # Verify that all parts consist of digits.
            if year.isdigit() and month.isdigit() and day.isdigit():
                # Check basic ranges (month 1-12, day 1-31).
                month_num = int(month)
                day_num = int(day)

                if 1 <= month_num <= 12 and 1 <= day_num <= 31:
                    return f"{day}.{month}.{year}"

    # Return original string if formatting fails.
    return date_string