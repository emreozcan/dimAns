from fractions import Fraction as _Fraction

from ..si_base.metre import nanometre as _nanometre
from ..metric_utils import make_metric_units as _make_metric_units

angstrom = (_Fraction(1, 10) * _nanometre).as_derived_unit("Å")

(
    quettaangstrom,
    yottaangstrom,
    zettaangstrom,
    exaangstrom,
    petaangstrom,
    teraangstrom,
    gigaangstrom,
    megaangstrom,
    kiloangstrom,
    hectoangstrom,
    decaangstrom,
    deciangstrom,
    centiangstrom,
    milliangstrom,
    microangstrom,
    nanoangstrom,
    picoangstrom,
    femtoangstrom,
    attoangstrom,
    zeptoangstrom,
    yoctoangstrom,
    rontoangstrom,
    quectoangstrom,
) = _make_metric_units(angstrom)

