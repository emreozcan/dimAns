from fractions import Fraction as _Fraction

from ..si_base.second import second as _second

minute = (60 * _second).as_derived_unit("min")
hour = (60 * minute).as_derived_unit("h")
day = (24 * hour).as_derived_unit("d")
week = (7 * day).as_derived_unit("w")
year = (_Fraction(364_2425, 1_0000) * day).as_derived_unit("y")
month = (_Fraction(1, 12) * year).as_derived_unit("mo")
