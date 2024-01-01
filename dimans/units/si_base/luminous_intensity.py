from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions

candela = _BaseUnit("cd", dimensions["luminous intensity"], _Fraction(1))

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
