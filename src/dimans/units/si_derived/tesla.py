from .weber import weber as _weber
from ..si_base.metre import metre as _metre
from ..metric_utils import make_metric_units as _make_metric_units

tesla = (_weber / _metre**2).as_derived_unit("T")

(
    quettatesla,
    yottatesla,
    zettatesla,
    exatesla,
    petatesla,
    teratesla,
    gigatesla,
    megatesla,
    kilotesla,
    hectotesla,
    decatesla,
    decitesla,
    centitesla,
    millitesla,
    microtesla,
    nanotesla,
    picotesla,
    femtotesla,
    attotesla,
    zeptotesla,
    yoctotesla,
    rontotesla,
    quectotesla,
) = _make_metric_units(tesla)
