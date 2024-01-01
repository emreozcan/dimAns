from fractions import Fraction as _Fraction
from ... import BaseUnit as _BaseUnit, Dimension as _Dimension

from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions

second = _BaseUnit("s", dimensions["time"], _Fraction(1))

(
    quettasecond,
    yottasecond,
    zettasecond,
    exasecond,
    petasecond,
    terasecond,
    gigasecond,
    megasecond,
    kilosecond,
    hectosecond,
    decasecond,
    decisecond,
    centisecond,
    millisecond,
    microsecond,
    nanosecond,
    picosecond,
    femtosecond,
    attosecond,
    zeptosecond,
    yoctosecond,
    rontosecond,
    quectosecond,
) = _make_metric_units(second)
