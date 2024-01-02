from .joule import joule as _joule
from ..si_base.gram import kilogram as _kilogram
from ..metric_utils import make_metric_units as _make_metric_units

gray = (_joule / _kilogram).as_derived_unit("Gy")

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
