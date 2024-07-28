from ..si_base.metre import metre as _metre
from ..metric_utils import make_metric_units as _make_metric_units

steradian = (_metre**2 / _metre**2).as_derived_unit("sr")

(
    quettasteradian,
    yottasteradian,
    zettasteradian,
    exasteradian,
    petasteradian,
    terasteradian,
    gigasteradian,
    megasteradian,
    kilosteradian,
    hectosteradian,
    decasteradian,
    decisteradian,
    centisteradian,
    millisteradian,
    microsteradian,
    nanosteradian,
    picosteradian,
    femtosteradian,
    attosteradian,
    zeptosteradian,
    yoctosteradian,
    rontosteradian,
    quectosteradian,
) = _make_metric_units(steradian)
