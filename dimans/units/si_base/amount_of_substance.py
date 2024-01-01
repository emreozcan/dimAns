from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions

mole = _BaseUnit("mol", dimensions["amount of substance"], _Fraction(1))

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
