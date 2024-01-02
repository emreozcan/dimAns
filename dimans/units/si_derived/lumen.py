from ..si_base.candela import candela as _candela
from .steradian import steradian as _steradian
from ..metric_utils import make_metric_units as _make_metric_units

lumen = (_candela * _steradian).as_derived_unit("lm")

(
    quettalumen,
    yottalumen,
    zettalumen,
    exalumen,
    petalumen,
    teralumen,
    gigalumen,
    megalumen,
    kilolumen,
    hectolumen,
    decalumen,
    decilumen,
    centilumen,
    millilumen,
    microlumen,
    nanolumen,
    picolumen,
    femtolumen,
    attolumen,
    zeptolumen,
    yoctolumen,
    rontolumen,
    quectolumen,
) = _make_metric_units(lumen)
