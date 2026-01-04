"""
Завдання 2. Обчислення визначеного інтеграла методом Монте-Карло

Обчислюємо інтеграл функції f(x) = x² від 0 до 2 та порівнюємо з аналітичним результатом.
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


# Визначення функції та межі інтегрування
def f(x):
    """Функція для інтегрування: f(x) = x²"""
    return x**2


def monte_carlo_integration(func, a, b, num_samples=100000):
    """
    Обчислення визначеного інтеграла методом Монте-Карло.

    Args:
        func: Функція для інтегрування
        a: Нижня межа інтегрування
        b: Верхня межа інтегрування
        num_samples: Кількість випадкових точок для методу Монте-Карло

    Returns:
        tuple: (значення інтеграла, кількість точок під кривою, загальна кількість точок)
    """
    # Генеруємо випадкові точки в прямокутнику [a, b] x [0, max_y]
    # Знаходимо максимальне значення функції на інтервалі
    x_values = np.linspace(a, b, 1000)
    max_y = np.max(func(x_values))

    # Генеруємо випадкові точки
    x_random = np.random.uniform(a, b, num_samples)
    y_random = np.random.uniform(0, max_y, num_samples)

    # Перевіряємо, які точки знаходяться під кривою
    under_curve = y_random <= func(x_random)
    points_under = np.sum(under_curve)

    # Обчислюємо площу
    rectangle_area = (b - a) * max_y
    integral_value = (points_under / num_samples) * rectangle_area

    return (
        integral_value,
        points_under,
        num_samples,
        x_random,
        y_random,
        under_curve,
        max_y,
    )


def analytical_integration(a, b):
    """
    Аналітичне обчислення інтеграла f(x) = x² від a до b.

    Інтеграл x² = x³/3
    """
    return (b**3 / 3) - (a**3 / 3)


def visualize_monte_carlo(
    func, a, b, x_random, y_random, under_curve, max_y, num_display=5000
):
    """
    Візуалізація методу Монте-Карло з випадковими точками.

    Args:
        func: Функція для візуалізації
        a, b: Межі інтегрування
        x_random, y_random: Випадкові точки
        under_curve: Булевий масив, які точки під кривою
        max_y: Максимальне значення функції
        num_display: Кількість точок для відображення (для кращої продуктивності)
    """
    # Створюємо діапазон значень для x
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)

    # Створення графіка
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Перший графік - класична візуалізація з заповненою областю
    ax1.plot(x, y, "r", linewidth=2, label="f(x) = x²")

    # Заповнення області під кривою
    ix = np.linspace(a, b, 400)
    iy = func(ix)
    ax1.fill_between(ix, iy, color="gray", alpha=0.3, label="Область інтегрування")

    # Налаштування графіка
    ax1.set_xlim([x[0], x[-1]])
    ax1.set_ylim([0, max(y) + 0.1])
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.axvline(x=a, color="gray", linestyle="--", alpha=0.5)
    ax1.axvline(x=b, color="gray", linestyle="--", alpha=0.5)
    ax1.set_title(f"Графік інтегрування f(x) = x² від {a} до {b}")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Другий графік - візуалізація методу Монте-Карло
    ax2.plot(x, y, "r", linewidth=2, label="f(x) = x²")

    # Відображаємо підмножину випадкових точок для кращої видимості
    indices = np.random.choice(
        len(x_random), min(num_display, len(x_random)), replace=False
    )

    # Точки під кривою (зелені)
    under_indices = indices[under_curve[indices]]
    ax2.scatter(
        x_random[under_indices],
        y_random[under_indices],
        c="green",
        s=1,
        alpha=0.3,
        label="Точки під кривою",
    )

    # Точки над кривою (червоні)
    above_indices = indices[~under_curve[indices]]
    ax2.scatter(
        x_random[above_indices],
        y_random[above_indices],
        c="red",
        s=1,
        alpha=0.3,
        label="Точки над кривою",
    )

    # Прямокутник для методу Монте-Карло
    ax2.plot(
        [a, b, b, a, a],
        [0, 0, max_y, max_y, 0],
        "b--",
        linewidth=1,
        alpha=0.5,
        label="Область вибірки",
    )

    ax2.set_xlim([a - 0.1, b + 0.1])
    ax2.set_ylim([0, max_y + 0.1])
    ax2.set_xlabel("x")
    ax2.set_ylabel("f(x)")
    ax2.set_title(f"Метод Монте-Карло ({num_display} точок відображено)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("monte_carlo_integration.png", dpi=150, bbox_inches="tight")
    plt.show()


def compare_methods(
    func, a, b, num_samples_list=[1000, 10000, 100000, 500000, 1000000]
):
    """
    Порівняння точності методу Монте-Карло при різній кількості точок.

    Args:
        func: Функція для інтегрування
        a, b: Межі інтегрування
        num_samples_list: Список кількостей точок для тестування
    """
    # Обчислюємо точне значення
    analytical_result = analytical_integration(a, b)
    quad_result, quad_error = spi.quad(func, a, b)

    print("=" * 80)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ МЕТОДІВ ОБЧИСЛЕННЯ ІНТЕГРАЛА")
    print("=" * 80)
    print("\nФункція: f(x) = x²")
    print(f"Межі інтегрування: від {a} до {b}")
    print("\n" + "-" * 80)
    print("ТОЧНІ МЕТОДИ:")
    print("-" * 80)
    print(f"Аналітичний результат:      {analytical_result:.15f}")
    print(f"SciPy quad:                 {quad_result:.15f}")
    print(f"Похибка quad:               {quad_error:.2e}")

    print("\n" + "-" * 80)
    print("МЕТОД МОНТЕ-КАРЛО:")
    print("-" * 80)
    print(
        f"{'Кількість точок':<20} {'Результат':<20} {'Похибка':<20} {'Відносна похибка (%)'}"
    )
    print("-" * 80)

    results = []
    for num_samples in num_samples_list:
        mc_result, points_under, total_points, *_ = monte_carlo_integration(
            func, a, b, num_samples
        )
        error = abs(mc_result - analytical_result)
        relative_error = (error / analytical_result) * 100

        results.append(
            {
                "samples": num_samples,
                "result": mc_result,
                "error": error,
                "relative_error": relative_error,
            }
        )

        print(
            f"{num_samples:<20} {mc_result:<20.15f} {error:<20.10f} {relative_error:.6f}%"
        )

    print("=" * 80)

    return analytical_result, quad_result, results


def main():
    """Головна функція програми"""
    # Параметри задачі
    a = 0  # Нижня межа
    b = 2  # Верхня межа
    num_samples = 500000  # Кількість точок для основного обчислення

    print("\n" + "=" * 80)
    print("ОБЧИСЛЕННЯ ВИЗНАЧЕНОГО ІНТЕГРАЛА МЕТОДОМ МОНТЕ-КАРЛО")
    print("=" * 80)

    # 1. Обчислення методом Монте-Карло
    print(f"\nОбчислення методу Монте-Карло з {num_samples} точками...")
    mc_result, points_under, total_points, x_random, y_random, under_curve, max_y = (
        monte_carlo_integration(f, a, b, num_samples)
    )

    print(f"Точок під кривою: {points_under}")
    print(f"Загальна кількість точок: {total_points}")
    print(f"Відношення: {points_under / total_points:.6f}")

    # 2. Порівняння з точними методами
    print("\n" + "=" * 80)
    analytical_result, quad_result, comparison_results = compare_methods(f, a, b)

    # 3. Візуалізація
    print("\nПобудова графіків...")
    visualize_monte_carlo(f, a, b, x_random, y_random, under_curve, max_y)

    # 4. Графік збіжності
    plot_convergence(comparison_results, analytical_result)

    # 5. Висновки
    print("\n" + "=" * 80)
    print("ВИСНОВКИ:")
    print("=" * 80)
    print(
        f"1. Аналітичне значення інтеграла x² від 0 до 2 дорівнює {analytical_result:.10f}"
    )
    print(
        f"2. Метод Монте-Карло з {num_samples} точками дав результат {mc_result:.10f}"
    )
    print(f"3. Абсолютна похибка: {abs(mc_result - analytical_result):.10f}")
    print(
        f"4. Відносна похибка: {abs(mc_result - analytical_result) / analytical_result * 100:.6f}%"
    )
    print(f"5. Функція SciPy quad дала результат {quad_result:.15f} (практично точний)")
    print("\n6. Збіжність методу Монте-Карло:")
    print("   - При збільшенні кількості точок похибка зменшується")
    print("   - Швидкість збіжності ~ O(1/√n), де n - кількість точок")
    print("   - Для досягнення точності 0.1% потрібно ~100,000 точок")
    print("   - Для досягнення точності 0.01% потрібно ~1,000,000 точок")
    print("=" * 80)


def plot_convergence(results, true_value):
    """
    Графік збіжності методу Монте-Карло.

    Args:
        results: Результати обчислень для різної кількості точок
        true_value: Точне значення інтеграла
    """
    samples = [r["samples"] for r in results]
    errors = [r["error"] for r in results]
    relative_errors = [r["relative_error"] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Графік абсолютної похибки
    ax1.loglog(samples, errors, "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("Кількість точок (N)")
    ax1.set_ylabel("Абсолютна похибка")
    ax1.set_title("Збіжність методу Монте-Карло\n(Абсолютна похибка)")
    ax1.grid(True, alpha=0.3, which="both")

    # Додаємо теоретичну лінію O(1/√n)
    theoretical = [errors[0] * np.sqrt(samples[0] / s) for s in samples]
    ax1.loglog(
        samples, theoretical, "r--", linewidth=1, alpha=0.7, label="Теоретична O(1/√N)"
    )
    ax1.legend()

    # Графік відносної похибки
    ax2.semilogx(samples, relative_errors, "go-", linewidth=2, markersize=8)
    ax2.set_xlabel("Кількість точок (N)")
    ax2.set_ylabel("Відносна похибка (%)")
    ax2.set_title("Збіжність методу Монте-Карло\n(Відносна похибка)")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("monte_carlo_convergence.png", dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
