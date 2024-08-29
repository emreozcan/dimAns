from ..si_base.second import second as _second
from ..si_base.mole import mole as _mole
from ..metric_utils import make_metric_units as _make_metric_units

katal = (_mole / _second).as_derived_unit("kat")

(
    quettakatal,
    yottakatal,
    zettakatal,
    exakatal,
    petakatal,
    terakatal,
    gigakatal,
    megakatal,
    kilokatal,
    hectokatal,
    decakatal,
    decikatal,
    centikatal,
    millikatal,
    microkatal,
    nanokatal,
    picokatal,
    femtokatal,
    attokatal,
    zeptokatal,
    yoctokatal,
    rontokatal,
    quectokatal,
) = _make_metric_units(katal)
