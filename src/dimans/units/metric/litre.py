from ... import DerivedUnit as _DerivedUnit
from ..si_base.metre import decimetre as _decimetre
from ..metric_utils import make_metric_units as _make_metric_units

litre = _DerivedUnit.using(_decimetre**3, "L")

(
    quettalitre,
    yottalitre,
    zettalitre,
    exalitre,
    petalitre,
    teralitre,
    gigalitre,
    megalitre,
    kilolitre,
    hectolitre,
    decalitre,
    decilitre,
    centilitre,
    millilitre,
    microlitre,
    nanolitre,
    picolitre,
    femtolitre,
    attolitre,
    zeptolitre,
    yoctolitre,
    rontolitre,
    quectolitre,
) = _make_metric_units(litre)
