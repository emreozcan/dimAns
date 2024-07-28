from fractions import Fraction

from ... import DerivedUnit
from ..si_base.kelvin import kelvin

__all__ = ["fahrenheit"]

fahrenheit = DerivedUnit("°F", {kelvin: Fraction(1)}, 5 / 9, 459.67)
