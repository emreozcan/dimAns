from fractions import Fraction as _Fraction
from typing import TypeVar as _TypeVar

import attrs as _attrs

from .. import BaseUnit as _BaseUnit, DerivedUnit as _DerivedUnit


@_attrs.define()
class MetricPrefix:
    name: str
    symbol: str
    factor: _Fraction


metric_prefixes = [
    MetricPrefix("quetta", "Q", _Fraction(10 ** 30)),
    MetricPrefix("yotta", "Y", _Fraction(10 ** 24)),
    MetricPrefix("zetta", "Z", _Fraction(10 ** 21)),
    MetricPrefix("exa", "E", _Fraction(10 ** 18)),
    MetricPrefix("peta", "P", _Fraction(10 ** 15)),
    MetricPrefix("tera", "T", _Fraction(10 ** 12)),
    MetricPrefix("giga", "G", _Fraction(10 ** 9)),
    MetricPrefix("mega", "M", _Fraction(10 ** 6)),
    MetricPrefix("kilo", "k", _Fraction(10 ** 3)),
    MetricPrefix("hecto", "h", _Fraction(10 ** 2)),
    MetricPrefix("deca", "da", _Fraction(10 ** 1)),
    MetricPrefix("deci", "d", _Fraction(1, 10 ** 1)),
    MetricPrefix("centi", "c", _Fraction(1, 10 ** 2)),
    MetricPrefix("milli", "m", _Fraction(1, 10 ** 3)),
    MetricPrefix("micro", "μ", _Fraction(1, 10 ** 6)),
    MetricPrefix("nano", "n", _Fraction(1, 10 ** 9)),
    MetricPrefix("pico", "p", _Fraction(1, 10 ** 12)),
    MetricPrefix("femto", "f", _Fraction(1, 10 ** 15)),
    MetricPrefix("atto", "a", _Fraction(1, 10 ** 18)),
    MetricPrefix("zepto", "z", _Fraction(1, 10 ** 21)),
    MetricPrefix("yocto", "y", _Fraction(1, 10 ** 24)),
    MetricPrefix("ronto", "r", _Fraction(1, 10 ** 27)),
    MetricPrefix("quecto", "q", _Fraction(1, 10 ** 30)),
]

_U = _TypeVar("_U", _BaseUnit, _DerivedUnit)


def make_metric_units(unit: _U) -> list[_U]:
    if isinstance(unit, _BaseUnit):
        return [
            _BaseUnit.using(
                unit,
                symbol=prefix.symbol + unit.symbol,
                factor=unit.si_factor * prefix.factor,
            )
            for prefix in metric_prefixes
        ]
    elif isinstance(unit, _DerivedUnit):
        return [
            _DerivedUnit.using(
                unit,
                symbol=prefix.symbol + unit.symbol,
                factor=unit.factor * prefix.factor,
            )
            for prefix in metric_prefixes
        ]
    else:
        raise TypeError(f"argument must be a BaseUnit or DerivedUnit, "
                        f"not {type(unit)}")
