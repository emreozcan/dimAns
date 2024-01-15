from ..si_base.second import second as _second
from ..metric_utils import make_metric_units as _make_metric_units

becquerel = (1 / _second).as_derived_unit("Bq")

(
    quettabecquerel,
    yottabecquerel,
    zettabecquerel,
    exabecquerel,
    petabecquerel,
    terabecquerel,
    gigabecquerel,
    megabecquerel,
    kilobecquerel,
    hectobecquerel,
    decabecquerel,
    decibecquerel,
    centibecquerel,
    millibecquerel,
    microbecquerel,
    nanobecquerel,
    picobecquerel,
    femtobecquerel,
    attobecquerel,
    zeptobecquerel,
    yoctobecquerel,
    rontobecquerel,
    quectobecquerel,
) = _make_metric_units(becquerel)
