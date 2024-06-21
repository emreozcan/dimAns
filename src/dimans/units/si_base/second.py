from ... import BaseUnit as _BaseUnit

from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

second = _BaseUnit("s", _dimensions["time"], 1)

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
