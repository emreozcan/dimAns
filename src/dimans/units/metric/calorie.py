from fractions import Fraction as _Fraction

from ..si_derived.joule import joule as _joule
from ..metric_utils import make_metric_units as _make_metric_units

calorie = (_Fraction(4184, 1000) * _joule).as_derived_unit("cal")

(
    quettacalorie,
    yottacalorie,
    zettacalorie,
    exacalorie,
    petacalorie,
    teracalorie,
    gigacalorie,
    megacalorie,
    kilocalorie,
    hectocalorie,
    decacalorie,
    decicalorie,
    centicalorie,
    millicalorie,
    microcalorie,
    nanocalorie,
    picocalorie,
    femtocalorie,
    attocalorie,
    zeptocalorie,
    yoctocalorie,
    rontocalorie,
    quectocalorie,
) = _make_metric_units(calorie)

