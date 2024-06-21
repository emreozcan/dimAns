from ... import BaseUnit as _BaseUnit
from ..metric_utils import make_metric_units as _make_metric_units
from ...dimension import dimensions as _dimensions

metre = _BaseUnit("m", _dimensions["length"], 1)

(
    quettametre,
    yottametre,
    zettametre,
    exametre,
    petametre,
    terametre,
    gigametre,
    megametre,
    kilometre,
    hectometre,
    decametre,
    decimetre,
    centimetre,
    millimetre,
    micrometre,
    nanometre,
    picometre,
    femtometre,
    attometre,
    zeptometre,
    yoctometre,
    rontometre,
    quectometre,
) = _make_metric_units(metre)
