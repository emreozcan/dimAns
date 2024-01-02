from ..si_base.second import second as _second
from .joule import joule as _joule
from ..metric_utils import make_metric_units as _make_metric_units

watt = (_joule / _second).as_derived_unit("W")

(
    quettawatt,
    yottawatt,
    zettawatt,
    exawatt,
    petawatt,
    terawatt,
    gigawatt,
    megawatt,
    kilowatt,
    hectowatt,
    decawatt,
    deciwatt,
    centiwatt,
    milliwatt,
    microwatt,
    nanowatt,
    picowatt,
    femtowatt,
    attowatt,
    zeptowatt,
    yoctowatt,
    rontowatt,
    quectowatt,
) = _make_metric_units(watt)
