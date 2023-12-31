from fractions import Fraction as _Fraction

from ... import BaseUnit as _BaseUnit
from ..si_base.mass import kilogram as _kilogram

pound = _BaseUnit.using(_kilogram, "lb", _Fraction(45359237, 100000000))

grain = _BaseUnit.using(pound, "gr", _Fraction(1, 7000))
drachm = _BaseUnit.using(pound, "dr", _Fraction(1, 256))
ounce = _BaseUnit.using(pound, "oz", _Fraction(1, 16))

stone = _BaseUnit.using(pound, "st", _Fraction(14))
quarter = _BaseUnit.using(pound, "qtr", _Fraction(28))
hundredweight = _BaseUnit.using(pound, "cwt", _Fraction(112))
ton = _BaseUnit.using(pound, "ton", _Fraction(2240))

slug = _BaseUnit.using(pound, "slug", _Fraction(1459390294, 100000000))
