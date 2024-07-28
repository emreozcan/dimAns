from ... import DerivedUnit as _DerivedUnit
from ..metric.litre import millilitre as _millilitre

gallon = _DerivedUnit.using(_millilitre, "gal", (454609 / 100))

fluid_ounce = _DerivedUnit.using(gallon, "fl_oz", (1 / 160))
gill = _DerivedUnit.using(fluid_ounce, "gi", 5)
pint = _DerivedUnit.using(fluid_ounce, "pt", 20)
quart = _DerivedUnit.using(fluid_ounce, "qt", 40)

# British apothecaries' volume measures
minim = _DerivedUnit.using(pint, "♏︎", (1 / 9600))
fluid_scruple = _DerivedUnit.using(pint, "fl ℈", (1 / 480))
fluid_drachm = _DerivedUnit.using(pint, "fl ʒ", (1 / 160))
