from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit
from ..imperial.mass import grain as _grain, pound as _pound

dram = _BaseUnit.using(_grain, "dr", _Fraction(875, 32))

us_hundredweight = _BaseUnit.using(_pound, "cwt", _Fraction(100))
us_ton = _BaseUnit.using(us_hundredweight, "ton", _Fraction(20))

pennyweight = _BaseUnit.using(_grain, "dwt", _Fraction(24))
troy_ounce = _BaseUnit.using(pennyweight, "oz t", _Fraction(20))
troy_pound = _BaseUnit.using(troy_ounce, "lb t", _Fraction(12))
