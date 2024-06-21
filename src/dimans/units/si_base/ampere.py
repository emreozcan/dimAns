from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

ampere = _BaseUnit("A", _dimensions["electric current"], 1)

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
