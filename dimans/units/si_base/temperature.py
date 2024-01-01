from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units

kelvin = _BaseUnit("K", _Dimension.TEMPERATURE, _Fraction(1))

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
