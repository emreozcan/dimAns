from ..si_base.metre import metre as _metre
from .newton import newton as _newton
from ..metric_utils import make_metric_units as _make_metric_units

pascal = (_newton / _metre**2).as_derived_unit("Pa")

(
    quettapascal,
    yottapascal,
    zettapascal,
    exapascal,
    petapascal,
    terapascal,
    gigapascal,
    megapascal,
    kilopascal,
    hectopascal,
    decapascal,
    decipascal,
    centipascal,
    millipascal,
    micropascal,
    nanopascal,
    picopascal,
    femtopascal,
    attopascal,
    zeptopascal,
    yoctopascal,
    rontopascal,
    quectopascal,
) = _make_metric_units(pascal)
