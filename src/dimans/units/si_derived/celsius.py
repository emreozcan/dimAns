from fractions import Fraction

from ... import DerivedUnit
from units.si_base.kelvin import kelvin

__all__ = [
    "celsius"
]

celsius = DerivedUnit(
    "°C",
    {kelvin: Fraction(1)},
    Fraction(1),
    Fraction(27315, 100)
)
