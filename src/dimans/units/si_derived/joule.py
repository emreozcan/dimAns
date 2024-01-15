from ..si_base.metre import metre as _metre
from .newton import newton as _newton
from ..metric_utils import make_metric_units as _make_metric_units

joule = (_newton * _metre).as_derived_unit("J")

(
    quettajoule,
    yottajoule,
    zettajoule,
    exajoule,
    petajoule,
    terajoule,
    gigajoule,
    megajoule,
    kilojoule,
    hectojoule,
    decajoule,
    decijoule,
    centijoule,
    millijoule,
    microjoule,
    nanojoule,
    picojoule,
    femtojoule,
    attojoule,
    zeptojoule,
    yoctojoule,
    rontojoule,
    quectojoule,
) = _make_metric_units(joule)
