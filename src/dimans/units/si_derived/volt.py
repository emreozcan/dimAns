from ..si_base.ampere import ampere as _ampere
from ..si_derived.watt import watt as _watt
from ..metric_utils import make_metric_units as _make_metric_units

volt = (_watt / _ampere).as_derived_unit("V")

(
    quettavolt,
    yottavolt,
    zettavolt,
    exavolt,
    petavolt,
    teravolt,
    gigavolt,
    megavolt,
    kilovolt,
    hectovolt,
    decavolt,
    decivolt,
    centivolt,
    millivolt,
    microvolt,
    nanovolt,
    picovolt,
    femtovolt,
    attovolt,
    zeptovolt,
    yoctovolt,
    rontovolt,
    quectovolt,
) = _make_metric_units(volt)
