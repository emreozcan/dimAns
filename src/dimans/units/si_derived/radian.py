from ..si_base.metre import metre as _metre
from ..metric_utils import make_metric_units as _make_metric_units

radian = (_metre / _metre).as_derived_unit("rad")

(
    quettaradian,
    yottaradian,
    zettaradian,
    exaradian,
    petaradian,
    teraradian,
    gigaradian,
    megaradian,
    kiloradian,
    hectoradian,
    decaradian,
    deciradian,
    centiradian,
    milliradian,
    microradian,
    nanoradian,
    picoradian,
    femtoradian,
    attoradian,
    zeptoradian,
    yoctoradian,
    rontoradian,
    quectoradian,
) = _make_metric_units(radian)
