from ..si_base.metre import metre as _metre
from ..imperial.length import inch as _inch
from ... import BaseUnit as _BaseUnit

pica = _BaseUnit.using(_inch, "P̸", (1 / 6))
point = _BaseUnit.using(pica, "pt", (1 / 12))
mil = _BaseUnit.using(_inch, "mil", (1 / 1000))
# twip is already defined in ..imperial.length

us_fathom = _BaseUnit.using(_metre, "ftm", (1143 / 625))
us_cable = _BaseUnit.using(us_fathom, "cable", 100)
us_nautical_mile = _BaseUnit.using(_metre, "nmi", 1852)

us_survey_link = _BaseUnit.using(_metre, "li", (792 / 3937))
us_survey_foot = _BaseUnit.using(_metre, "ft", (1200 / 3937))
us_survey_rod = _BaseUnit.using(_metre, "rd", (19800 / 3937))
us_survey_chain = _BaseUnit.using(_metre, "ch", (79200 / 3937))
us_survey_furlong = _BaseUnit.using(_metre, "fur", (792000 / 3937))
us_survey_mile = _BaseUnit.using(_metre, "mi", (6336000 / 3937))
us_survey_league = _BaseUnit.using(_metre, "lea", (19008000 / 3937))
