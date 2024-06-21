from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

kelvin = _BaseUnit("K", _dimensions["thermodynamic temperature"], 1)

(
    quettakelvin,
    yottakelvin,
    zettakelvin,
    exakelvin,
    petakelvin,
    terakelvin,
    gigakelvin,
    megakelvin,
    kilokelvin,
    hectokelvin,
    decakelvin,
    decikelvin,
    centikelvin,
    millikelvin,
    microkelvin,
    nanokelvin,
    picokelvin,
    femtokelvin,
    attokelvin,
    zeptokelvin,
    yoctokelvin,
    rontokelvin,
    quectokelvin,
) = _make_metric_units(kelvin)
