from .joule import joule as _joule
from ..si_base.gram import kilogram as _kilogram
from ..metric_utils import make_metric_units as _make_metric_units

sievert = (_joule / _kilogram).as_derived_unit("Gy")

(
    quettasievert,
    yottasievert,
    zettasievert,
    exasievert,
    petasievert,
    terasievert,
    gigasievert,
    megasievert,
    kilosievert,
    hectosievert,
    decasievert,
    decisievert,
    centisievert,
    millisievert,
    microsievert,
    nanosievert,
    picosievert,
    femtosievert,
    attosievert,
    zeptosievert,
    yoctosievert,
    rontosievert,
    quectosievert,
) = _make_metric_units(sievert)
