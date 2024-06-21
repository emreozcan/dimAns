from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

mole = _BaseUnit("mol", _dimensions["amount of substance"], 1)

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
