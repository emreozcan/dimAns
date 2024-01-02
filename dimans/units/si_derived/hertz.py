from ..si_base.second import second as _second
from ..metric_utils import make_metric_units as _make_metric_units

hertz = (1 / _second).as_derived_unit("Hz")

(
    quettahertz,
    yottahertz,
    zettahertz,
    exahertz,
    petahertz,
    terahertz,
    gigahertz,
    megahertz,
    kilohertz,
    hectohertz,
    decahertz,
    decihertz,
    centihertz,
    millihertz,
    microhertz,
    nanohertz,
    picohertz,
    femtohertz,
    attohertz,
    zeptohertz,
    yoctohertz,
    rontohertz,
    quectohertz,
) = _make_metric_units(hertz)
