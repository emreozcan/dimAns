from ..si_derived.joule import joule as _joule
from ..si_base.ampere import ampere as _ampere
from ..metric_utils import make_metric_units as _make_metric_units

weber = (_joule / _ampere).as_derived_unit("Wb")

(
    quettaweber,
    yottaweber,
    zettaweber,
    exaweber,
    petaweber,
    teraweber,
    gigaweber,
    megaweber,
    kiloweber,
    hectoweber,
    decaweber,
    deciweber,
    centiweber,
    milliweber,
    microweber,
    nanoweber,
    picoweber,
    femtoweber,
    attoweber,
    zeptoweber,
    yoctoweber,
    rontoweber,
    quectoweber,
) = _make_metric_units(weber)
