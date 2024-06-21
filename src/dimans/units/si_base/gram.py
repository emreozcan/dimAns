from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

gram = _BaseUnit("g", _dimensions["mass"], 1)

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
