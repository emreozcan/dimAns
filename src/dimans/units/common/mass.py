from fractions import Fraction as _Fraction

from ..si_base.gram import kilogram as _kilogram

dalton = (_Fraction(1660539066605, 10**39) * _kilogram).as_derived_unit("Da")
