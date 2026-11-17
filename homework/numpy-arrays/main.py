from decimal import Decimal

import numpy as np


def task01():
    a = np.arange(60).reshape(3, 4, 5)
    print(a.shape, a.ndim, a.size, a.dtype, a.strides, a.flags.c_contiguous)
    print("Strides — сдвиги в байтах по трём осям. Размер: 3 × 4 × 5 = 60.")


def task02():
    a = np.array([1, 2, 3, 4])
    print(a / 2, a // 2, a / 2.0)
    print(a.dtype, (a / 2).dtype, (a // 2).dtype)
    b = np.array([1, 2, 3], dtype=np.int8)
    result = b + 127
    print(result, result.dtype)
    print("Деление создаёт новый массив. int8 переполняется по модулю 256.")


def task03():
    x, y = float(np.float32(0.1)), float(np.float64(0.1))
    for value in (x, y):
        error = value - 0.1
        print(repr(error), f"{error:.20e}")
    exact = Decimal("0.1")
    ratio = abs(Decimal.from_float(x) - exact) / abs(Decimal.from_float(y) - exact)
    print(f"Отношение ошибок к точному 0.1: {ratio:.0f}")
    print("Вычитание двух одинаковых float64 даёт ноль. float32 допустим при достаточной точности, но рискован при накоплении ошибок.")


def task04():
    shape = (2, 3)
    for a in (np.zeros(shape, np.float64), np.zeros(shape, np.float32),
              np.ones(shape, np.int16), np.full(shape, 7, np.uint8)):
        print(a.dtype, a.nbytes)
    print("Экономия:", 1000 * 1000 * (np.dtype(np.float64).itemsize - np.dtype(np.float32).itemsize), "байт")
    print("float32 занимает вдвое меньше памяти, но хранит меньше значащих цифр.")


def task05():
    a = np.arange(24)
    current = a
    for shape in ((4, 6), (2, 3, 4), (2, 2, 6), (24,)):
        current = current.reshape(shape)
        print(current.shape, np.array_equal(a, current.ravel()))
    print("reshape меняет форму и шаги. Копия нужна, если новое расположение невозможно описать шагами исходного массива.")


def task06():
    m = np.arange(12).reshape(3, 4)
    f, r = m.flatten(), m.ravel()
    print(f.base is None, r.base is not None)
    f[0] = 999
    print(m[0, 0])
    r[1] = 888
    print(m[0, 1])
    print("ravel старается сохранить общую память. flatten всегда даёт отдельную копию.")


def task07():
    v = np.arange(5)
    print(v[:, None].shape, "столбец")
    print(v[None, :].shape, "строка")
    print(np.squeeze(v[:, None]).shape, "удалена ось длины 1")
    transposed = np.arange(6).reshape(2, 3).T
    print(transposed.shape, transposed, "строки и столбцы поменялись местами")
    table = v[:, None] + v[None, :]
    print(table.shape, table, "таблица попарных сумм")


def task08():
    a = np.arange(6).reshape(2, 3)
    b = a.T
    print(b.base is not None, np.shares_memory(a, b))
    b[0, 1] = 999
    print(a)
    print(a.strides, b.strides, "Транспонирование меняет местами шаги, сохраняя память.")


def task09():
    a = np.arange(6).reshape(2, 3)
    b = np.arange(6).reshape(3, 2)
    for value in (a @ b, a.T @ b.T, a * a):
        print(value.shape, value)
    try:
        a * b
    except ValueError:
        print("Формы (2, 3) и (3, 2) несовместимы для поэлементного умножения.")
    diagonal = np.diag([2, 3])
    print("Для одинаковых диагональных матриц:", np.array_equal(diagonal * diagonal, diagonal @ diagonal))
    print("* умножает элементы, @ вычисляет скалярное произведение строк и столбцов.")


def task10():
    m = np.arange(12).reshape(3, 4)
    for name, operation in (("Сумма", np.sum), ("Среднее", np.mean), ("Индекс максимума", np.argmax)):
        print(name, "по столбцам:", operation(m, axis=0))
        print(name, "по строкам:", operation(m, axis=1))
    assert np.array_equal(m.sum(axis=0), m[0] + m[1] + m[2])


def task11():
    x = np.random.default_rng(42).normal(size=(5, 3))
    mean = x.mean(axis=0)
    mean_keep = x.mean(axis=0, keepdims=True)
    print(mean.shape, mean_keep.shape, (x - mean).shape, (x - mean_keep).shape)
    print(x.std(axis=1).shape, x.std(axis=1, keepdims=True).shape)
    z = (x - x.mean(axis=1, keepdims=True)) / x.std(axis=1, keepdims=True)
    print(z.mean(axis=1), z.std(axis=1))
    assert np.allclose(z.mean(axis=1), 0) and np.allclose(z.std(axis=1), 1)
    print("keepdims оставляет ось длины 1, чтобы результат по каждой строке применялся к её элементам.")


def task12():
    a = np.arange(10)
    b = a[2:5]
    b[0] = 999
    print(a)
    c = a[2:5].copy()
    c[0] = -1
    print(a)
    print("Срез экономит память при чтении. Для независимого изменения данных нужна копия, иначе меняется исходная выборка.")


def task13():
    a = np.random.default_rng(0).normal(size=20)
    print(a[a > 0].size, a[(a > -1) & (a < 1)].size)
    print(a[[0, 5, 10, 15]], a[np.abs(a) > 2])
    a[a < 0] = 0
    print(a)
    print("Оператор & объединяет две булевы маски. a[a > 0] уже содержит отобранные вещественные числа другой длины.")


def task14():
    x = np.random.default_rng(1).normal(size=(100, 3))
    z = (x - x.mean(axis=0)) / x.std(axis=0)
    print(z.mean(axis=0), z.std(axis=0))
    distances = np.linalg.norm(z[:, None, :] - z[None, :, :], axis=2)
    print(distances.shape, np.allclose(distances.diagonal(), 0), np.allclose(distances, distances.T))
    assert distances.shape == (100, 100) and np.allclose(distances.diagonal(), 0)
    assert np.allclose(distances, distances.T)


def task15():
    raw = np.random.default_rng(42).normal(20, 2, size=(30, 4))
    raw[7, 2] = 100
    print(raw.shape, raw.dtype, raw.size)
    outliers = np.abs(raw - raw.mean(axis=0)) > 3 * raw.std(axis=0)
    print("Выбросов:", outliers.sum(), "координаты:", np.argwhere(outliers).tolist())
    with_nan = raw.copy()
    with_nan[outliers] = np.nan
    clean = np.where(np.isnan(with_nan), np.nanmean(with_nan, axis=0), with_nan)
    print("Значения после замены:", clean[outliers])
    print(clean.T.shape, np.array_equal(clean.T.T, clean))
    flat = clean.ravel()
    print(flat.shape, np.array_equal(flat.reshape(30, 4), clean))
    means, stds = clean.mean(axis=0), clean.std(axis=0)
    print(means, stds)
    z = (clean - means) / stds
    print(z.mean(axis=0), z.std(axis=0))
    assert outliers[7, 2] and np.isfinite(clean).all()
    assert np.allclose(z.mean(axis=0), 0) and np.allclose(z.std(axis=0), 1)
    print("Копия сохраняет исходные измерения при замене выбросов на NaN.")
    print("Статистика датчиков применяется ко всем строкам через broadcasting.")
    print("После транспонирования статистику по датчикам пришлось бы считать по другой оси.")


if __name__ == "__main__":
    tasks = (task01, task02, task03, task04, task05, task06, task07, task08,
             task09, task10, task11, task12, task13, task14, task15)
    for number, task in enumerate(tasks, 1):
        print(f"\nЗадача {number}")
        task()
