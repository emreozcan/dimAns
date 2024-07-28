from ... import BaseUnit as _BaseUnit
from ..si_base.gram import kilogram as _kilogram

pound = _BaseUnit.using(_kilogram, "lb", (45359237 / 100000000))

grain = _BaseUnit.using(pound, "gr", (1 / 7000))
drachm = _BaseUnit.using(pound, "dr", (1 / 256))
ounce = _BaseUnit.using(pound, "oz", (1 / 16))

stone = _BaseUnit.using(pound, "st", 14)
quarter = _BaseUnit.using(pound, "qtr", 28)
hundredweight = _BaseUnit.using(pound, "cwt", 112)
ton = _BaseUnit.using(pound, "ton", 2240)

slug = _BaseUnit.using(pound, "slug", (1459390294 / 100000000))
