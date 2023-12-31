from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit, Dimension as _Dimension
from ..metric_utils import make_metric_units as _make_metric_units

mole = _BaseUnit("mol", _Dimension.AMOUNT_OF_SUBSTANCE, _Fraction(1))

(
    quettamole,
    yottamole,
    zettamole,
    examole,
    petamole,
    teramole,
    gigamole,
    megamole,
    kilomole,
    hectomole,
    decamole,
    decimole,
    centimole,
    millimole,
    micromole,
    nanomole,
    picomole,
    femtomole,
    attomole,
    zeptomole,
    yoctomole,
    rontomole,
    quectomole,
) = _make_metric_units(mole)
