from ..si_base.time import second as _second
from ..si_base.amount_of_substance import mole as _mole
from ..metric_utils import make_metric_units as _make_metric_units

gray = (_mole / _second).as_derived_unit("Gy")

(
    quettagray,
    yottagray,
    zettagray,
    exagray,
    petagray,
    teragray,
    gigagray,
    megagray,
    kilogray,
    hectogray,
    decagray,
    decigray,
    centigray,
    milligray,
    microgray,
    nanogray,
    picogray,
    femtogray,
    attogray,
    zeptogray,
    yoctogray,
    rontogray,
    quectogray,
) = _make_metric_units(gray)
