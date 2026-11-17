import math
import random
from decimal import Decimal
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent


def relative_error(approx, exact):
    return abs(approx - exact) / abs(exact) if exact else math.inf


def added(values):
    total = 0.0
    for value in values:
        total += value
    return total


def compare(approx, exact):
    return abs(approx - exact), relative_error(approx, exact)


print("Задача 2")
for name, approx, exact, unit in (
    ("Мост", 1247, 1250, "м"),
    ("Болт", 9.7, 10.0, "мм"),
):
    absolute, relative = compare(approx, exact)
    print(f"{name}: Δ = {absolute:.3g} {unit}, δ = {relative:.2%}")
print("После перевода в одинаковые единицы абсолютная ошибка больше у моста. В процентах больше отклонение диаметра болта, потому что его точный размер гораздо меньше.")

print("\nЗадача 3")
for approx, exact in ((3.14, math.pi), (2.718, math.e), (9.8, 9.81), (0.333, 1 / 3)):
    print(f"{approx}: {relative_error(approx, exact):.8%}")
assert relative_error(1, 0) == math.inf
print("Деление на модуль точного значения даёт относительную ошибку. При точном значении 0 функция возвращает inf по условию.")

print("\nЗадача 4")
approx, tolerance = 47.3, 0.001
print(f"[{approx / (1+tolerance):.7f}, {approx / (1-tolerance):.7f}]")
print("Поскольку точное значение находится в знаменателе определения ошибки, границы получаются делением на 1 ± 0.001. Интервал немного несимметричен.")

print("\nЗадача 5")
print(f"Датчик B гарантирует Δ не более 0.3 °C при |T| ≤ {0.3 / 0.005:.0f} °C.")
print("Ниже порога по модулю у B меньше предельная абсолютная ошибка. Выше порога меньше предел у A.")

print("\nЗадача 6")
for original, scientific, count in (
    ("0.004520", "4.520 × 10⁻³", 4),
    ("1200", "1.2 × 10³", "от 2 до 4"),
    ("1.200", "1.200 × 10⁰", 4),
    ("10.03", "1.003 × 10¹", 4),
    ("0.03050", "3.050 × 10⁻²", 4),
    ("250000", "2.5 × 10⁵", "от 2 до 6"),
):
    print(f"{original}: {scientific}, значащих цифр: {count}")
print("Для 1200 и 250000 приведена запись с минимальным числом значащих цифр. Конечные нули целого числа неоднозначны, а нули в мантиссе показывают заявленную точность.")

print("\nЗадача 7")
print(f"{4.738291:.2f} ± 0.02, 3 значащие цифры")
print("Последний разряд результата — сотые, как у погрешности. Дальнейшие цифры создавали бы впечатление избыточной точности.")

print("\nЗадача 8")
print([round(x) for x in (0.5, 1.5, 2.5, 3.5, -0.5, -1.5, -2.5)])
rng = random.Random(42)
even_sum = up_sum = 0
for _ in range(1_000_000):
    k = rng.randrange(10)
    even_sum += round(k + 0.5)
    up_sum += k + 1
print("Разность округлений на выборке:", up_sum - even_sum)
print("Ожидаемый сдвиг округления вверх:", 1_000_000 * 0.5)
print("Python при равном расстоянии выбирает чётное целое. Округление всех половин вверх систематически завышает итог при массовых операциях.")

print("\nЗадача 9")
terms = [1 / k for k in range(1, 101)]
reference = math.fsum(terms)
full = added(terms)
rounded = added(round(x, 3) for x in terms)
for name, result in (("Без округления", full), ("По три знака", rounded)):
    print(name, result, compare(result, reference))
base = abs(full - reference)
print("Рост ошибки:", abs(rounded - reference) / base if base else "эталон совпал с первым результатом")
print("Округление каждого слагаемого меняет исходные данные. Округлять лучше итог при выводе.")

print("\nЗадача 10")
result = 0.1 + 0.2
print(repr(result), result == 0.3, math.isclose(result, 0.3), compare(result, 0.3))
print("В двоичной записи 0.1 имеет бесконечное повторение. В памяти хранится ближайшее представимое значение. После сложения и округления результат оказывается рядом с 0.3.")

print("\nЗадача 11")
difference = (1 + 1e-15) - 1
b = 1e8
root = math.sqrt(b * b - 4)
direct, stable = (-b + root) / 2, -2 / (b + root)
bd = Decimal(10**8)
reference_dec = -2 / (bd + (bd * bd - 4).sqrt())
print(difference, compare(difference, 1e-15))
for name, value in (("Прямой корень", direct), ("Устойчивый корень", stable)):
    print(name, value, compare(Decimal.from_float(value), reference_dec))
print("При вычитании близких чисел теряются общие цифры. Устойчивый корень вычисляется через произведение корней и не требует вычитать близкие величины.")

print("\nЗадача 12")
data = [0.1] * 1_000_000
print("Метод | Сумма | Δ | δ")
for method in (added, sum, math.fsum):
    value = method(data)
    print(method.__name__, value, *compare(value, 100_000), sep=" | ")
print("fsum совпадает с эталоном в этом запуске. При нулевой измеренной ошибке отношение ошибок к ней не определено.")

print("\nЗадача 13")
small, large = [1e-10] * 500_000, [1e6] * 500_000
reference = math.fsum(small + large)
for label, values in (("Малые сначала", small + large), ("Большие сначала", large + small)):
    print(label, *compare(added(values), reference))
print("Если сначала накапливать большие значения, малые слагаемые не сдвигают округлённую сумму. Суммирование малых первым шагом сохраняет их совместный вклад.")

print("\nЗадача 14")
steps, errors = [], []
thresholds = {1e-9: None, 1e-6: None, 1e-3: None}
value = 1.0
for step in range(1, 10_001):
    value *= 1.0001
    error = relative_error(value, math.exp(step * math.log(1.0001)))
    steps.append(step)
    errors.append(error)
    for threshold in thresholds:
        if thresholds[threshold] is None and error > threshold:
            thresholds[threshold] = step
for threshold, step in thresholds.items():
    print(threshold, step if step is not None else "не превышен")
plt.plot(steps, errors)
plt.xlabel("Шаг")
plt.ylabel("Относительная погрешность")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(ROOT / "growth-error.svg")
plt.close()
print("Конечная ошибка:", errors[-1], "максимум:", max(errors))
print("Округление накапливается, но ошибка колеблется. На 10 000 шагах ни один заданный порог не достигнут.")

print("\nЗадача 15")
float_balance = 0.0
decimal_balance = Decimal("0.00")
penny_balance = 0
penny = Decimal("0.01")
for _ in range(1_000_000):
    float_balance += 0.01
    decimal_balance += penny
    penny_balance += 1
difference = Decimal.from_float(float_balance) - decimal_balance
print("float:", float_balance, "Decimal:", decimal_balance, "целые копейки:", penny_balance)
print("Расхождение в рублях:", difference, "в процентах:", difference / decimal_balance * 100)
assert decimal_balance == Decimal(penny_balance) / 100
print("Decimal и целочисленный счёт дают ровно 10 000 рублей. Десятичная копейка не представляется точно в float, поэтому многократные начисления накапливают ошибку.")
