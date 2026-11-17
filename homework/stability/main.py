import math
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

mp.mp.dps = 60
ROOT = Path(__file__).resolve().parent


def relative(value, reference):
    return float(abs(mp.mpf(float(value)) - reference) / abs(reference))


def compare(rows, first, second, reference):
    print("x | прямой результат | устойчивый результат | эталон | прямая ошибка | устойчивая ошибка")
    records = []
    for x in rows:
        a, b, ref = first(x), second(x), reference(mp.mpf(x))
        e1, e2 = relative(a, ref), relative(b, ref)
        records.append((x, e1, e2))
        print(f"{x:.2e} | {a:.10e} | {b:.10e} | {float(ref):.10e} | {e1:.3e} | {e2:.3e}")
    return records


def naive_sum(values):
    total = 0.0
    for value in values:
        total += value
    return total


def bad_cos(x):
    return (1 - math.cos(x)) / (x * x)


def good_cos(x):
    return 2 * (math.sin(x / 2) / x) ** 2


def ref_cos(x):
    return 2 * (mp.sin(x / 2) / x) ** 2


def bad_root(x):
    return math.sqrt(x + 1) - math.sqrt(x)


def good_root(x):
    return 1 / (math.sqrt(x + 1) + math.sqrt(x))


def ref_root(x):
    return mp.sqrt(x + 1) - mp.sqrt(x)


print("2. Вычитание близких чисел")
a, b, da = 1 + 1e-8, 1.0, 1e-9
diff = a - b
changed = (a + da) - b
print("|a/(a-b)|, |b/(a-b)|:", abs(a / diff), abs(b / diff))
print("Δf/δa:", (changed - diff) / da)
print("Относительное изменение:", abs(changed - diff) / abs(diff))
print("Предсказание:", abs(a / diff) * da / abs(a))
print("Производные по a и b равны 1 и −1. Абсолютный отклик на изменение a близок к единице, но относительно малой разности изменение составляет около 10%.")

print("\n3. Кратные корни")
print("ε | корни | сдвиг | предыдущий сдвиг / текущий")
previous = None
for epsilon in (1e-2, 1e-4, 1e-6):
    shift = math.sqrt(epsilon)
    print(epsilon, (1 - shift, 1 + shift), shift, previous / shift if previous else "—")
    previous = shift
print("Замена ε в 100 раз меняет сдвиг в 10 раз. Возмущение коэффициента порождает сдвиг порядка √ε, поэтому кратный корень чувствителен.")

print("\n4. Обусловленность и устойчивость")
compare((1e-2, 1e-6, 1e-10, 1e-16), lambda x: (1 + x) ** 2 - 1,
        lambda x: x * (2 + x), lambda x: x * (2 + x))
print("У f(x)=2x+x² относительное число обусловленности близко к 1 при малых положительных x. Прямой алгоритм теряет цифры из-за округления 1+x и последующего вычитания.")

print("\n5. Малый по модулю корень")
compare((1e4, 1e8, 1e12), lambda b: (-b + math.sqrt(b * b - 4)) / 2,
        lambda b: -2 / (b + math.sqrt(b * b - 4)),
        lambda b: -2 / (b + mp.sqrt(b * b - 4)))
print("При b=10⁸ прямой способ уже теряет заметную часть точности. При b=10¹² разность округляется до нуля, а формула через произведение корней сохраняет точность.")

print("\n6. Косинус при малых x")
cos_rows = compare((1e-2, 1e-4, 1e-6, 1e-8, 1e-10), bad_cos, good_cos, ref_cos)
first_over = next(x for x, error, _ in cos_rows if error > 0.01)
print(f"На проверенной сетке ошибка впервые больше 1% при x={first_over:.0e}. При вычитании почти равных величин лучше заменить разность алгебраическим тождеством.")

print("\n7. Разность квадратных корней")
root_rows = compare((1e4, 1e8, 1e12, 1e14, 1e16), bad_root, good_root, ref_root)
x1, e1, _ = root_rows[0]
x2, e2, _ = root_rows[-2]
print(f"Оценка показателя по крайним точкам до насыщения: {math.log(e2/e1)/math.log(x2/x1):.2f}. Масштаб роста близок к линейному, но округление даёт разброс.")

print("\n8. Логарифм")
compare((1e-2, 1e-8, 1e-12, 1e-16), lambda x: math.log(1 + x), math.log1p, mp.log1p)
print("log1p вычисляет логарифм с учётом исходного малого x. В прямой формуле сложение может округлиться до 1 ещё до вызова log; специальные функции избегают такой потери.")

print("\n9. Гармоническая сумма")
print("n | цикл | sum | fsum (относительные ошибки)")
harmonic_errors = []
for n in (10**5, 10**6, 10**7):
    ref = mp.harmonic(n)
    results = [relative(method(1.0 / k for k in range(1, n + 1)), ref)
               for method in (naive_sum, sum, math.fsum)]
    harmonic_errors.append(results[0])
    print(n, *(f"{error:.3e}" for error in results), sep=" | ")
slope = math.log10(harmonic_errors[-1] / harmonic_errors[0]) / 2
print(f"Измеренный наклон между 10⁵ и 10⁷: {slope:.2f}. В проверенном диапазоне порог 10⁻¹⁰ не превышен, но обычное последовательное сложение теряет больше точности.")

print("\n10. Источники ошибки")
x = 1e-4
x32 = np.float32(x)
value32 = (np.float32(1) - np.cos(x32)) / (x32 * x32)
ref = ref_cos(mp.mpf(x))
print("Фактор | до | после | log10(после/до)")
for label, before, after in (
    ("x: 1e-2 → 1e-8", cos_rows[0][1], cos_rows[3][1]),
    ("float64 → float32", relative(bad_cos(x), ref), relative(value32, ref)),
    ("прямой → устойчивый", relative(bad_cos(x), ref), relative(good_cos(x), ref)),
):
    print(label, f"{before:.3e}", f"{after:.3e}", f"{math.log10(after/before):.2f}", sep=" | ")
print("Малый аргумент усиливает сокращение, float32 даёт меньше точных цифр, а замена формулы восстанавливает их без смены типа.")

print("\n11. Независимый эталон")
x = 1e16
v1 = math.sqrt(x + 1) - math.sqrt(x)
upper_root = math.sqrt(x + 1)
v2 = (upper_root ** 2 - x) / (upper_root + math.sqrt(x))
reference = ref_root(mp.mpf(x))
print(v1 == v2, v1, v2, mp.nstr(reference, 18), relative(v1, reference), relative(v2, reference))
print("В обеих реализациях промежуточная сумма округлилась до x. Совпадение двух float не подтверждает правильность без независимого эталона.")

print("\n12. Диапазон значений")
rows = compare(np.logspace(2, 16, 15).tolist(), bad_root, good_root, ref_root)
xs, bad, good = np.array(rows).T
fit = (xs <= 1e14) & (bad > 0)
measured = np.polyfit(np.log10(xs[fit]), np.log10(bad[fit]), 1)[0]
plt.loglog(xs, bad, "o-", label="Прямая формула")
plt.loglog(xs, good, "s-", label="Устойчивая формула")
plt.loglog(xs, np.finfo(float).eps * xs, "--", label="ε × x")
plt.xlabel("x")
plt.ylabel("Относительная ошибка")
plt.grid(True, which="major", alpha=0.25)
plt.legend()
plt.tight_layout()
plt.savefig(ROOT / "root-errors.svg")
plt.close()
print(f"Наклон на диапазоне до насыщения: {measured:.2f}. Ожидаемый порядок наклона — 1; отдельные точки могут отклоняться из-за округления.")

print("\n13. Воспроизводимость")
def experiment(seed):
    random.seed(seed)
    sources = ([random.random() for _ in range(100_000)],
               np.random.default_rng(seed).random(100_000).tolist())
    return [(sum(values), math.fsum(values), float(np.sum(values))) for values in sources]

print("Python", sys.version.split()[0], "NumPy", np.__version__)
first = experiment(42)
assert first == experiment(42)
for seed, result in ((42, first), (43, experiment(43))):
    for source, (ordinary, precise, numpy_sum) in zip(("random", "default_rng"), result):
        print(seed, source, ordinary, precise, numpy_sum,
              f"Δsum={ordinary - precise:.3e}", f"Δnp={numpy_sum - precise:.3e}")
print("Повтор seed=42 воспроизводит и суммы, и расхождения. Знак расхождения может зависеть от данных, а воспроизводимость требует фиксировать генератор, seed и версии.")

print("\n14. Границы представимости")
def formatted(method, values):
    try:
        return str(method(values))
    except (OverflowError, ValueError) as error:
        return type(error).__name__

finite = [1e300, 1e-300, 0.0, 1e-320]
scenarios = {
    "Конечные": finite,
    "Субнормальные": [1e-320, 1e-320],
    "Сокращение": [1e300, 1e-300, -1e300, 1e-320],
    "+inf": finite + [math.inf],
    "nan": finite + [math.nan],
    "Разные бесконечности": [math.inf, -math.inf],
    "Переполнение": [1e308, 1e308],
}
for name, values in scenarios.items():
    print(name, formatted(naive_sum, values), formatted(math.fsum, values), sep=" | ")
print("NaN распространяется в обоих способах. Одна бесконечность даёт бесконечность; противоположные бесконечности и переполнение требуют проверки и обработки исключений.")

print("\n15. Эксперимент для log(1+x)")
print("Цель: сравнить точность двух формул на логарифмической сетке. Эталон — mpmath, 60 десятичных знаков.")
compare(np.logspace(-16, -2, 15).tolist(), lambda x: math.log(1 + x), math.log1p, mp.log1p)
print("Для x около 10⁻² прямая формула ещё пригодна, если допустима накопленная ошибка. При x порядка 10⁻¹⁶ округление 1+x полностью теряет x, а log1p остаётся близкой к точности float64.")
