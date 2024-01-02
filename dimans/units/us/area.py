from fractions import Fraction as _Fraction

from ..us.length import us_survey_league as _us_survey_league
from ... import DerivedUnit as _DerivedUnit

us_survey_township = _DerivedUnit.using(
    _us_survey_league ** 2, "twp.", _Fraction(4)
)
