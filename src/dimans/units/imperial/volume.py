from fractions import Fraction as _Fraction

from ... import DerivedUnit as _DerivedUnit
from ...units.metric.litre import millilitre as _millilitre

gallon = _DerivedUnit.using(_millilitre, "gal", _Fraction(454609, 100))

fluid_ounce = _DerivedUnit.using(gallon, "fl_oz", _Fraction(1, 160))
gill = _DerivedUnit.using(fluid_ounce, "gi", _Fraction(5))
pint = _DerivedUnit.using(fluid_ounce, "pt", _Fraction(20))
quart = _DerivedUnit.using(fluid_ounce, "qt", _Fraction(40))

# British apothecaries' volume measures
minim = _DerivedUnit.using(pint, "♏︎", _Fraction(1, 9600))
fluid_scruple = _DerivedUnit.using(pint, "fl ℈", _Fraction(1, 480))
fluid_drachm = _DerivedUnit.using(pint, "fl ʒ", _Fraction(1, 160))
