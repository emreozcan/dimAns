from fractions import Fraction

import attrs

from ..abc import Unit

__all__ = [
    "MetricPrefix",
    "metric_prefixes",
    "make_metric_units",
]


@attrs.define()
class MetricPrefix:
    name: str
    symbol: str
    factor: Fraction


metric_prefixes = [
    MetricPrefix("quetta", "Q", Fraction(10 ** 30)),
    MetricPrefix("yotta", "Y", Fraction(10 ** 24)),
    MetricPrefix("zetta", "Z", Fraction(10 ** 21)),
    MetricPrefix("exa", "E", Fraction(10 ** 18)),
    MetricPrefix("peta", "P", Fraction(10 ** 15)),
    MetricPrefix("tera", "T", Fraction(10 ** 12)),
    MetricPrefix("giga", "G", Fraction(10 ** 9)),
    MetricPrefix("mega", "M", Fraction(10 ** 6)),
    MetricPrefix("kilo", "k", Fraction(10 ** 3)),
    MetricPrefix("hecto", "h", Fraction(10 ** 2)),
    MetricPrefix("deca", "da", Fraction(10 ** 1)),
    MetricPrefix("deci", "d", Fraction(1, 10 ** 1)),
    MetricPrefix("centi", "c", Fraction(1, 10 ** 2)),
    MetricPrefix("milli", "m", Fraction(1, 10 ** 3)),
    MetricPrefix("micro", "μ", Fraction(1, 10 ** 6)),
    MetricPrefix("nano", "n", Fraction(1, 10 ** 9)),
    MetricPrefix("pico", "p", Fraction(1, 10 ** 12)),
    MetricPrefix("femto", "f", Fraction(1, 10 ** 15)),
    MetricPrefix("atto", "a", Fraction(1, 10 ** 18)),
    MetricPrefix("zepto", "z", Fraction(1, 10 ** 21)),
    MetricPrefix("yocto", "y", Fraction(1, 10 ** 24)),
    MetricPrefix("ronto", "r", Fraction(1, 10 ** 27)),
    MetricPrefix("quecto", "q", Fraction(1, 10 ** 30)),
]


def make_metric_units(unit: Unit) -> list[Unit]:
    return [
        unit.using(
            unit,
            symbol=prefix.symbol + unit.symbol,
            factor=unit.factor * prefix.factor,
        )
        for prefix in metric_prefixes
    ]
