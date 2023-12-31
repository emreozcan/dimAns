from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units

candela = _BaseUnit("cd", _Dimension.LUMINOUS_INTENSITY, _Fraction(1))

(
    quettacandela,
    yottacandela,
    zettacandela,
    exacandela,
    petacandela,
    teracandela,
    gigacandela,
    megacandela,
    kilocandela,
    hectocandela,
    decacandela,
    decicandela,
    centicandela,
    millicandela,
    microcandela,
    nanocandela,
    picocandela,
    femtocandela,
    attocandela,
    zeptocandela,
    yoctocandela,
    rontocandela,
    quectocandela,
) = _make_metric_units(candela)
