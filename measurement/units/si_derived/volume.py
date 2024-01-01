from ... import DerivedUnit as _DerivedUnit
from ..si_base.length import decimeter
from ..metric_utils import make_metric_units as _make_metric_units

liter = _DerivedUnit.using(decimeter ** 3, "L")

(
    quettaliter,
    yottaliter,
    zettaliter,
    exaliter,
    petaliter,
    teraliter,
    gigaliter,
    megaliter,
    kiloliter,
    hectoliter,
    decaliter,
    deciliter,
    centiliter,
    milliliter,
    microliter,
    nanoliter,
    picoliter,
    femtoliter,
    attoliter,
    zeptoliter,
    yoctoliter,
    rontoliter,
    quectoliter,
) = _make_metric_units(liter)

