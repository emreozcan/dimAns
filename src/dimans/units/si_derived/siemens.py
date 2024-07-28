from .ohm import ohm as _ohm
from ..metric_utils import make_metric_units as _make_metric_units

siemens = (1 / _ohm).as_derived_unit("S")

(
    quettasiemens,
    yottasiemens,
    zettasiemens,
    exasiemens,
    petasiemens,
    terasiemens,
    gigasiemens,
    megasiemens,
    kilosiemens,
    hectosiemens,
    decasiemens,
    decisiemens,
    centisiemens,
    millisiemens,
    microsiemens,
    nanosiemens,
    picosiemens,
    femtosiemens,
    attosiemens,
    zeptosiemens,
    yoctosiemens,
    rontosiemens,
    quectosiemens,
) = _make_metric_units(siemens)
