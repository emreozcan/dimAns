from ..common.energy import erg as _erg
from ..si_base.gram import kilogram as _kilogram, gram as _gram
from ..si_derived import coulomb as _coulomb, sievert as _sievert
from ..si_derived.becquerel import (
    gigabecquerel as _gigabecquerel,
    megabecquerel as _megabecquerel,
)

curie = (37 * _gigabecquerel).as_derived_unit("Ci")
rutherford = _megabecquerel.as_derived_unit("Rd")
rontgen = ((258 * 10**-6) * _coulomb / _kilogram).as_derived_unit("R")
rad = (100 * _erg / _gram).as_derived_unit("rad")
rontgen_equivalent_man = (0.01 * _sievert).as_derived_unit("rem")
