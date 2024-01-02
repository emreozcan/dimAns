from ..si_base.mass import kilogram as _kilogram
from ..si_base.length import metre as _metre
from ..si_base.time import second as _second
from ..metric_utils import make_metric_units as _make_metric_units

newton = (_kilogram * _metre / _second ** 2).as_derived_unit("N")

(
    quettanewton,
    yottanewton,
    zettanewton,
    exanewton,
    petanewton,
    teranewton,
    giganewton,
    meganewton,
    kilonewton,
    hectonewton,
    decanewton,
    decinewton,
    centinewton,
    millinewton,
    micronewton,
    nanonewton,
    piconewton,
    femtonewton,
    attonewton,
    zeptonewton,
    yoctonewton,
    rontonewton,
    quectonewton,
) = _make_metric_units(newton)
