from decimal import Decimal


def errors(estimate: Decimal, reference: Decimal):
    absolute = abs(estimate - reference)
    relative = absolute / abs(reference) if reference else None
    return absolute, relative


def main():
    measurements = (
        ("A, м", "2.48", "2.50"),
        ("B, м", "0.247", "0.250"),
        ("C, м", "-0.51", "-0.50"),
        ("D, м", "0.01", "0"),
    )
    print("Показание | Измерение | Эталон | Абс., м | Отн., %")
    for name, estimate, reference in measurements:
        absolute, relative = errors(Decimal(estimate), Decimal(reference))
        percent = "не определена" if relative is None else f"{100 * relative:.2f}"
        print(name, estimate, reference, absolute, percent, sep=" | ")


if __name__ == "__main__":
    main()
