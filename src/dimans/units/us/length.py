from ..si_base.metre import metre as _metre
from ..imperial.length import inch as _inch
from ... import BaseUnit as _BaseUnit

pica = _BaseUnit.using(_inch, "P̸", (1 / 6))
point = _BaseUnit.using(pica, "pt", (1 / 12))
mil = _BaseUnit.using(_inch, "mil", (1 / 1000))
# twip is already defined in ..imperial.length

us_fathom = _BaseUnit.using(_metre, "US ftm", (1143 / 625))
us_cable = _BaseUnit.using(us_fathom, "US cable", 100)
us_nautical_mile = _BaseUnit.using(_metre, "US nmi", 1852)

us_survey_link = _BaseUnit.using(_metre, "survey li", (792 / 3937))
us_survey_foot = _BaseUnit.using(_metre, "survey ft", (1200 / 3937))
us_survey_rod = _BaseUnit.using(_metre, "survey rd", (19800 / 3937))
us_survey_chain = _BaseUnit.using(_metre, "survey ch", (79200 / 3937))
us_survey_furlong = _BaseUnit.using(_metre, "survey fur", (792000 / 3937))
us_survey_mile = _BaseUnit.using(_metre, "survey mi", (6336000 / 3937))
us_survey_league = _BaseUnit.using(_metre, "survey lea", (19008000 / 3937))
