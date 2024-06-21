from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

candela = _BaseUnit("cd", _dimensions["luminous intensity"], 1)

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
