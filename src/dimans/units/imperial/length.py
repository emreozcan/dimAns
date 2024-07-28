from ... import BaseUnit as _BaseUnit
from ..si_base.metre import metre as _metre

foot = _BaseUnit.using(_metre, "ft", (381 / 1250))

twip = _BaseUnit.using(foot, "twip", (1 / 17280))
thou = _BaseUnit.using(foot, "th", (1 / 12000))
barleycorn = _BaseUnit.using(foot, "barleycorn", (1 / 36))
inch = _BaseUnit.using(foot, "in", (1 / 12))
hand = _BaseUnit.using(foot, "hh", (1 / 3))

yard = _BaseUnit.using(foot, "yd", 3)
chain = _BaseUnit.using(foot, "ch", 66)
furlong = _BaseUnit.using(foot, "fur", 660)
mile = _BaseUnit.using(foot, "mi", 5280)
league = _BaseUnit.using(foot, "lea", 15840)

# Maritime units
fathom = _BaseUnit.using(_metre, "ftm", (1852 / 1000))
cable = _BaseUnit.using(fathom, "cable", 100)
nautical_mile = _BaseUnit.using(cable, "nmi", 10)

# Gunter's survey units
link = _BaseUnit.using(foot, "link", (66 / 100))
rod = _BaseUnit.using(link, "rod", 25)
