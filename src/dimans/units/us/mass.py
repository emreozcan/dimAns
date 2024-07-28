from ... import BaseUnit as _BaseUnit
from ..imperial.mass import grain as _grain, pound as _pound

dram = _BaseUnit.using(_grain, "dr", (875 / 32))

us_hundredweight = _BaseUnit.using(_pound, "cwt", 100)
us_ton = _BaseUnit.using(us_hundredweight, "ton", 20)

pennyweight = _BaseUnit.using(_grain, "dwt", 24)
troy_ounce = _BaseUnit.using(pennyweight, "oz t", 20)
troy_pound = _BaseUnit.using(troy_ounce, "lb t", 12)
