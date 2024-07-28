from math import pi as _pi

from ..si_base.metre import metre as _metre
from ..metric_utils import make_metric_units as _make_metric_units


parsec = (96_939_420_213_600_000 / _pi * _metre).as_derived_unit("pc")

(
    quettaparsec,
    yottaparsec,
    zettaparsec,
    exaparsec,
    petaparsec,
    teraparsec,
    gigaparsec,
    megaparsec,
    kiloparsec,
    hectoparsec,
    decaparsec,
    deciparsec,
    centiparsec,
    milliparsec,
    microparsec,
    nanoparsec,
    picoparsec,
    femtoparsec,
    attoparsec,
    zeptoparsec,
    yoctoparsec,
    rontoparsec,
    quectoparsec,
) = _make_metric_units(parsec)
