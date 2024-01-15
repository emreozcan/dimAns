from .coulomb import coulomb as _coulomb
from .volt import volt as _volt
from ..metric_utils import make_metric_units as _make_metric_units

farad = (_coulomb / _volt).as_derived_unit("F")

(
    quettafarad,
    yottafarad,
    zettafarad,
    exafarad,
    petafarad,
    terafarad,
    gigafarad,
    megafarad,
    kilofarad,
    hectofarad,
    decafarad,
    decifarad,
    centifarad,
    millifarad,
    microfarad,
    nanofarad,
    picofarad,
    femtofarad,
    attofarad,
    zeptofarad,
    yoctofarad,
    rontofarad,
    quectofarad,
) = _make_metric_units(farad)
