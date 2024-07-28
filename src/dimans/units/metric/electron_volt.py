from ..si_derived.joule import joule as _joule
from ..metric_utils import make_metric_units as _make_metric_units


electron_volt = ((1.602_176_634 / (10**19)) * _joule).as_derived_unit("eV")

(
    quettaelectron_volt,
    yottaelectron_volt,
    zettaelectron_volt,
    exaelectron_volt,
    petaelectron_volt,
    teraelectron_volt,
    gigaelectron_volt,
    megaelectron_volt,
    kiloelectron_volt,
    hectoelectron_volt,
    decaelectron_volt,
    decielectron_volt,
    centielectron_volt,
    millielectron_volt,
    microelectron_volt,
    nanoelectron_volt,
    picoelectron_volt,
    femtoelectron_volt,
    attoelectron_volt,
    zeptoelectron_volt,
    yoctoelectron_volt,
    rontoelectron_volt,
    quectoelectron_volt,
) = _make_metric_units(electron_volt)
