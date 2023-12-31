from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units

ampere = _BaseUnit("A", _Dimension.ELECTRIC_CURRENT, _Fraction(1))

(
    quettaampere,
    yottaampere,
    zettaampere,
    exaampere,
    petaampere,
    teraampere,
    gigaampere,
    megaampere,
    kiloampere,
    hectoampere,
    decaampere,
    deciampere,
    centiampere,
    milliampere,
    microampere,
    nanoampere,
    picoampere,
    femtoampere,
    attoampere,
    zeptoampere,
    yoctoampere,
    rontoampere,
    quectoampere,
) = _make_metric_units(ampere)
