from ..metric.litre import microlitre as _microlitre, litre as _litre
from ..imperial.length import inch as _inch
from ... import DerivedUnit as _DerivedUnit

us_minim = _DerivedUnit.using(
    _microlitre, "US min", (61_611_519_921_875 / 10_000_000_000_00)
)

us_fluid_dram = (60 * us_minim).as_derived_unit("fl dr")
us_teaspoon = (80 * us_minim).as_derived_unit("tsp")
us_tablespoon = (3 * us_teaspoon).as_derived_unit("tbsp")
us_fluid_ounce = (2 * us_tablespoon).as_derived_unit("fl oz")
us_shot = (3 * us_tablespoon).as_derived_unit("jig")
us_gill = (4 * us_fluid_ounce).as_derived_unit("US gi")
us_cup = (8 * us_fluid_ounce).as_derived_unit("c")
us_pint_liquid = (2 * us_cup).as_derived_unit("US pint liq.")
us_quart_liquid = (2 * us_pint_liquid).as_derived_unit("US qt liq.")
us_pottle_liquid = (2 * us_quart_liquid).as_derived_unit("pot")
us_gallon_liquid = (4 * us_quart_liquid).as_derived_unit("US gal liq.")
us_barrel_liquid = ((31.5 * us_gallon_liquid)).as_derived_unit("US bbl liq.")
oil_barrel = (42 * us_gallon_liquid).as_derived_unit("US bbl oil")
hogshead = (63 * us_gallon_liquid).as_derived_unit("hogshead")

us_pint_dry = _DerivedUnit.using(_litre, "US pint dry", (5506104713575 / 10000000000000))
us_quart_dry = (2 * us_pint_dry).as_derived_unit("US qt dry")
us_gallon_dry = (4 * us_quart_dry).as_derived_unit("US gal dry")
peck = (2 * us_gallon_dry).as_derived_unit("pk")
bushel = (4 * peck).as_derived_unit("bu")
us_barrel_dry = (7056 * _inch**3).as_derived_unit("US bbl dry")
