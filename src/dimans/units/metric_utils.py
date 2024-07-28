import dataclasses
from collections.abc import Sequence
from fractions import Fraction
from typing import TypeVar

from ..base_classes import Unit
from .. import BaseUnit, DerivedUnit

__all__ = [
    "MetricPrefix",
    "metric_prefixes",
    "binary_metric_prefixes",
    "make_metric_units",
    "make_binary_metric_units",
    "map_to_units",
]


@dataclasses.dataclass(frozen=True)
class MetricPrefix:
    name: str
    symbol: str
    factor: Fraction


metric_prefixes = [
    MetricPrefix("quetta", "Q", Fraction(10**30)),
    MetricPrefix("yotta", "Y", Fraction(10**24)),
    MetricPrefix("zetta", "Z", Fraction(10**21)),
    MetricPrefix("exa", "E", Fraction(10**18)),
    MetricPrefix("peta", "P", Fraction(10**15)),
    MetricPrefix("tera", "T", Fraction(10**12)),
    MetricPrefix("giga", "G", Fraction(10**9)),
    MetricPrefix("mega", "M", Fraction(10**6)),
    MetricPrefix("kilo", "k", Fraction(10**3)),
    MetricPrefix("hecto", "h", Fraction(10**2)),
    MetricPrefix("deca", "da", Fraction(10**1)),
    MetricPrefix("deci", "d", Fraction(1, 10**1)),
    MetricPrefix("centi", "c", Fraction(1, 10**2)),
    MetricPrefix("milli", "m", Fraction(1, 10**3)),
    MetricPrefix("micro", "μ", Fraction(1, 10**6)),
    MetricPrefix("nano", "n", Fraction(1, 10**9)),
    MetricPrefix("pico", "p", Fraction(1, 10**12)),
    MetricPrefix("femto", "f", Fraction(1, 10**15)),
    MetricPrefix("atto", "a", Fraction(1, 10**18)),
    MetricPrefix("zepto", "z", Fraction(1, 10**21)),
    MetricPrefix("yocto", "y", Fraction(1, 10**24)),
    MetricPrefix("ronto", "r", Fraction(1, 10**27)),
    MetricPrefix("quecto", "q", Fraction(1, 10**30)),
]

binary_metric_prefixes = [
    MetricPrefix("kibi", "Ki", Fraction(2**10)),
    MetricPrefix("mebi", "Mi", Fraction(2**20)),
    MetricPrefix("gibi", "Gi", Fraction(2**30)),
    MetricPrefix("tebi", "Ti", Fraction(2**40)),
    MetricPrefix("pebi", "Pi", Fraction(2**50)),
    MetricPrefix("exbi", "Ei", Fraction(2**60)),
    MetricPrefix("zebi", "Zi", Fraction(2**70)),
    MetricPrefix("yobi", "Yi", Fraction(2**80)),
]


AnyUnit = TypeVar("AnyUnit", Unit, BaseUnit, DerivedUnit)


def map_to_units(
    unit: AnyUnit, prefix_list: Sequence[MetricPrefix]
) -> list[AnyUnit]:
    if unit.symbol is None:
        raise ValueError("Unit must have a symbol")

    if not isinstance(unit, BaseUnit):
        return [
            (unit * float(prefix.factor)).as_derived_unit(
                prefix.symbol + unit.symbol
            )
            for prefix in prefix_list
        ]
    return [
        BaseUnit(
            symbol=prefix.symbol + unit.symbol,
            factor=float(prefix.factor * unit.factor),
            dimension=unit.dimension,
        )
        for prefix in prefix_list
    ]


def make_metric_units(unit: AnyUnit) -> list[AnyUnit]:
    return map_to_units(unit, metric_prefixes)


def make_binary_metric_units(unit: AnyUnit) -> list[AnyUnit]:
    return map_to_units(unit, binary_metric_prefixes)
