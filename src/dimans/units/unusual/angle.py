from fractions import Fraction as _Fraction
from math import pi as _pi

from ..common.angle import turn as _turn
from ..si_derived.radian import radian as _radian

furman = (_Fraction(1, 65536) * _turn).as_derived_unit("furman")
gradian = (_Fraction(1, 200) * _pi * _radian).as_derived_unit("grad")

nato_mil = (_Fraction(1, 6_400) * _turn).as_derived_unit("NATO mil")
warsaw_pact_mil = (
    _Fraction(1, 6_000) * _turn).as_derived_unit("Warsaw Pact mil")
