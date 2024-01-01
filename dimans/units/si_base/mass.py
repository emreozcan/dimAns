from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions

gram = _BaseUnit("g", dimensions["mass"], _Fraction(1))

(
    quettagram,
    yottagram,
    zettagram,
    exagram,
    petagram,
    teragram,
    gigagram,
    megagram,
    kilogram,
    hectogram,
    decagram,
    decigram,
    centigram,
    milligram,
    microgram,
    nanogram,
    picogram,
    femtogram,
    attogram,
    zeptogram,
    yoctogram,
    rontogram,
    quectogram,
) = _make_metric_units(gram)
