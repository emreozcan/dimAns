from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions

meter = _BaseUnit("m", dimensions["length"], _Fraction(1))

(
    quettameter,
    yottameter,
    zettameter,
    exameter,
    petameter,
    terameter,
    gigameter,
    megameter,
    kilometer,
    hectometer,
    decameter,
    decimeter,
    centimeter,
    millimeter,
    micrometer,
    nanometer,
    picometer,
    femtometer,
    attometer,
    zeptometer,
    yoctometer,
    rontometer,
    quectometer,
) = _make_metric_units(meter)
