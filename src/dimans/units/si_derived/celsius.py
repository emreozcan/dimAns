from fractions import Fraction

from ... import DerivedUnit
from ..si_base.kelvin import kelvin

__all__ = ["celsius"]

celsius = DerivedUnit("°C", {kelvin: Fraction(1)}, 1, 273.15)
