from fractions import Fraction

from ... import DerivedUnit
from ..si_base.kelvin import kelvin

__all__ = [
    "celsius"
]

celsius = DerivedUnit(
    "°F",
    {kelvin: Fraction(1)},
    Fraction(5, 9),
    Fraction(45967, 100)
)
