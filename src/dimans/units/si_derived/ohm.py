from ..si_derived.volt import volt as _volt
from ..si_base.ampere import ampere as _ampere
from ..metric_utils import make_metric_units as _make_metric_units

ohm = (_volt / _ampere).as_derived_unit("Ω")

(
    quettaohm,
    yottaohm,
    zettaohm,
    exaohm,
    petaohm,
    teraohm,
    gigaohm,
    megaohm,
    kiloohm,
    hectoohm,
    decaohm,
    deciohm,
    centiohm,
    milliohm,
    microohm,
    nanoohm,
    picoohm,
    femtoohm,
    attoohm,
    zeptoohm,
    yoctoohm,
    rontoohm,
    quectoohm,
) = _make_metric_units(ohm)
