"""
Завдання 1. Оптимізація виробництва напоїв

Мета: Максимізувати загальну кількість вироблених напоїв ("Лимонад" та "Фруктовий сік")
з урахуванням обмежень на ресурси.

Умови:
- Лимонад: потребує 2 од. Води, 1 од. Цукру, 1 од. Лимонного соку
- Фруктовий сік: потребує 2 од. Фруктового пюре, 1 од. Води
- Обмеження ресурсів: 100 од. Води, 50 од. Цукру, 30 од. Лимонного соку, 40 од. Фруктового пюре
"""

from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value


def optimize_production():
    """
    Створює та розв'язує модель лінійного програмування для оптимізації виробництва напоїв.

    Returns:
        tuple: (кількість лимонаду, кількість фруктового соку, загальна кількість продуктів)
    """

    # Створюємо модель оптимізації
    model = LpProblem(name="beverage-production-optimization", sense=LpMaximize)

    # Змінні рішення (кількість продуктів для виробництва)
    # lowBound=0 означає, що не можемо виробити від'ємну кількість
    lemonade = LpVariable(name="Lemonade", lowBound=0, cat="Integer")
    fruit_juice = LpVariable(name="Fruit_Juice", lowBound=0, cat="Integer")

    # Цільова функція: максимізувати загальну кількість вироблених продуктів
    model += lemonade + fruit_juice, "Total_Products"

    # Обмеження на ресурси
    # Вода: 2 од. на Лимонад + 1 од. на Фруктовий сік <= 100 од.
    model += (2 * lemonade + 1 * fruit_juice <= 100, "Water_constraint")

    # Цукор: 1 од. на Лимонад <= 50 од.
    model += (1 * lemonade <= 50, "Sugar_constraint")

    # Лимонний сік: 1 од. на Лимонад <= 30 од.
    model += (1 * lemonade <= 30, "Lemon_juice_constraint")

    # Фруктове пюре: 2 од. на Фруктовий сік <= 40 од.
    model += (2 * fruit_juice <= 40, "Fruit_puree_constraint")

    # Розв'язуємо модель
    model.solve()

    # Виводимо результати
    print("=" * 70)
    print("РЕЗУЛЬТАТИ ОПТИМІЗАЦІЇ ВИРОБНИЦТВА НАПОЇВ")
    print("=" * 70)
    print(f"\nСтатус розв'язку: {LpStatus[model.status]}")

    # Оптимальне рішення
    lemonade_qty = value(lemonade)
    fruit_juice_qty = value(fruit_juice)
    total_products = value(model.objective)

    print(f"\n{'Оптимальний план виробництва:':-^70}")
    print(f"  • Лимонад: {lemonade_qty:.0f} одиниць")
    print(f"  • Фруктовий сік: {fruit_juice_qty:.0f} одиниць")
    print(f"  • Загальна кількість продуктів: {total_products:.0f} одиниць")

    # Аналіз використання ресурсів
    water_used = 2 * lemonade_qty + 1 * fruit_juice_qty
    sugar_used = 1 * lemonade_qty
    lemon_juice_used = 1 * lemonade_qty
    fruit_puree_used = 2 * fruit_juice_qty

    print(f"\n{'Використання ресурсів:':-^70}")
    print(f"  • Вода: {water_used:.0f} / 100 од. ({water_used / 100 * 100:.1f}%)")
    print(f"  • Цукор: {sugar_used:.0f} / 50 од. ({sugar_used / 50 * 100:.1f}%)")
    print(
        f"  • Лимонний сік: {lemon_juice_used:.0f} / 30 од. ({lemon_juice_used / 30 * 100:.1f}%)"
    )
    print(
        f"  • Фруктове пюре: {fruit_puree_used:.0f} / 40 од. ({fruit_puree_used / 40 * 100:.1f}%)"
    )

    # Аналіз обмежень
    print(f"\n{'Аналіз обмежень (Slack Analysis):':-^70}")
    water_slack = 100 - water_used
    sugar_slack = 50 - sugar_used
    lemon_slack = 30 - lemon_juice_used
    puree_slack = 40 - fruit_puree_used

    print(
        f"  • Вода: {water_slack:.0f} од. залишається (обмеження {'активне' if water_slack == 0 else 'неактивне'})"
    )
    print(
        f"  • Цукор: {sugar_slack:.0f} од. залишається (обмеження {'активне' if sugar_slack == 0 else 'неактивне'})"
    )
    print(
        f"  • Лимонний сік: {lemon_slack:.0f} од. залишається (обмеження {'активне' if lemon_slack == 0 else 'неактивне'})"
    )
    print(
        f"  • Фруктове пюре: {puree_slack:.0f} од. залишається (обмеження {'активне' if puree_slack == 0 else 'неактивне'})"
    )

    # Висновки
    print(f"\n{'ВИСНОВКИ:':-^70}")
    bottlenecks = []
    if water_slack == 0:
        bottlenecks.append("Вода")
    if sugar_slack == 0:
        bottlenecks.append("Цукор")
    if lemon_slack == 0:
        bottlenecks.append("Лимонний сік")
    if puree_slack == 0:
        bottlenecks.append("Фруктове пюре")

    if bottlenecks:
        print(f"  • Обмежуючі ресурси (bottleneck): {', '.join(bottlenecks)}")
        print("  • Збільшення цих ресурсів дозволить виробляти більше продукції")
    else:
        print("  • Немає обмежуючих ресурсів - всі ресурси використані неповністю")

    print("=" * 70)

    return lemonade_qty, fruit_juice_qty, total_products


if __name__ == "__main__":
    # Перевіряємо, чи встановлено PuLP
    try:
        import pulp

        print("✓ Бібліотека PuLP встановлена\n")
    except ImportError:
        print("✗ Бібліотека PuLP не встановлена!")
        print("Встановіть її за допомогою: pip install pulp")
        exit(1)

    # Запускаємо оптимізацію
    lemonade_qty, fruit_juice_qty, total = optimize_production()
