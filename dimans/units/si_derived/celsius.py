from fractions import Fraction

from dimans import DerivedUnit
from dimans.units.si_base.kelvin import kelvin

__all__ = [
    "celsius"
]

celsius = DerivedUnit(
    "°C",
    {kelvin: Fraction(1)},
    Fraction(1),
    Fraction(27315, 100)
)
