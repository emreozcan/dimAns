from .ohm import ohm as _ohm
from ..si_base.second import second as _second
from ..metric_utils import make_metric_units as _make_metric_units

henry = (_ohm * _second).as_derived_unit("H")

(
    quettahenry,
    yottahenry,
    zettahenry,
    exahenry,
    petahenry,
    terahenry,
    gigahenry,
    megahenry,
    kilohenry,
    hectohenry,
    decahenry,
    decihenry,
    centihenry,
    millihenry,
    microhenry,
    nanohenry,
    picohenry,
    femtohenry,
    attohenry,
    zeptohenry,
    yoctohenry,
    rontohenry,
    quectohenry,
) = _make_metric_units(henry)
