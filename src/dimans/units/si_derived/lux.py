from .lumen import lumen as _lumen
from ..si_base.metre import metre as _metre
from ..metric_utils import make_metric_units as _make_metric_units

lux = (_lumen / _metre**2).as_derived_unit("lx")

(
    quettalux,
    yottalux,
    zettalux,
    exalux,
    petalux,
    teralux,
    gigalux,
    megalux,
    kilolux,
    hectolux,
    decalux,
    decilux,
    centilux,
    millilux,
    microlux,
    nanolux,
    picolux,
    femtolux,
    attolux,
    zeptolux,
    yoctolux,
    rontolux,
    quectolux,
) = _make_metric_units(lux)
