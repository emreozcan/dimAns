from fractions import Fraction as _Fraction

from ..si_base.metre import metre as _metre
from ..imperial.length import inch as _inch
from ... import BaseUnit as _BaseUnit

pica = _BaseUnit.using(_inch, "P̸", _Fraction(1, 6))
point = _BaseUnit.using(pica, "pt", _Fraction(1, 12))
mil = _BaseUnit.using(_inch, "mil", _Fraction(1, 1000))
# twip is already defined in ..imperial.length

us_fathom = _BaseUnit.using(_metre, "ftm", _Fraction(1143, 625))
us_cable = _BaseUnit.using(us_fathom, "cable", _Fraction(100))
us_nautical_mile = _BaseUnit.using(_metre, "nmi", _Fraction(1852))

us_survey_link = _BaseUnit.using(_metre, "li", _Fraction(792, 3937))
us_survey_foot = _BaseUnit.using(_metre, "ft", _Fraction(1200, 3937))
us_survey_rod = _BaseUnit.using(_metre, "rd", _Fraction(19800, 3937))
us_survey_chain = _BaseUnit.using(_metre, "ch", _Fraction(79200, 3937))
us_survey_furlong = _BaseUnit.using(_metre, "fur", _Fraction(792000, 3937))
us_survey_mile = _BaseUnit.using(_metre, "mi", _Fraction(6336000, 3937))
us_survey_league = _BaseUnit.using(_metre, "lea", _Fraction(19008000, 3937))
