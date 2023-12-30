from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from fractions import Fraction
from numbers import Number

import attrs


@attrs.define(slots=True, frozen=True, eq=False)
class Quantity:
    value: Number
    unit: Unit


@attrs.define(slots=True, frozen=True, eq=False)
class Unit:
    base_unit_exponents: Mapping[Dimension, BaseUnitExponent]


@attrs.define(slots=True, frozen=True, eq=False)
class BaseUnitExponent:
    """Represents a base unit raised to some exponent."""

    base_unit: BaseUnit
    exponent: Fraction


@attrs.define(slots=True, frozen=True, eq=False, repr=False)
class BaseUnit:
    """A unit of measurement which only has one dimension of power 1."""

    symbol: str
    """The symbol of the unit.

    This value is used to generate human-readable representations of
    quantities."""

    dimension: Dimension
    """The dimension of the unit."""

    si_factor: Fraction
    """The factor by which the base SI unit of the dimension is multiplied by.
    """

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.symbol}>"

    def get_conversion_factor_to(self, other: BaseUnit, /):
        if not isinstance(other, BaseUnit):
            raise TypeError(f"expected BaseUnit, "
                            f"got {other.__class__.__name__}")
        if self.dimension != other.dimension:
            raise ValueError(f"cannot convert {self.dimension} unit to "
                             f"{other.dimension} unit")
        return self.si_factor / other.si_factor

    def get_conversion_factor_from(self, other: BaseUnit, /):
        if not isinstance(other, BaseUnit):
            raise TypeError(f"expected BaseUnit, "
                            f"got {other.__class__.__name__}")
        if self.dimension != other.dimension:
            raise ValueError(f"cannot convert {self.dimension} unit to "
                             f"{other.dimension} unit")
        return other.si_factor / self.si_factor


class Dimension(Enum):
    ONE = "1"
    MASS = "M"
    LENGTH = "L"
    LUMINOUS_INTENSITY = "J"
    TIME = "T"
    ELECTRIC_CURRENT = "I"
    TEMPERATURE = "Θ"
    AMOUNT_OF_SUBSTANCE = "N"


g = BaseUnit("g", Dimension.MASS, Fraction(1, 1000))
kg = BaseUnit("kg", Dimension.MASS, Fraction(1))
nm = BaseUnit("nm", Dimension.LENGTH, Fraction(1, 1_000_000_000))
um = BaseUnit("µm", Dimension.LENGTH, Fraction(1, 1_000_000))
mm = BaseUnit("mm", Dimension.LENGTH, Fraction(1, 1000))
cm = BaseUnit("cm", Dimension.LENGTH, Fraction(1, 100))
m = BaseUnit("m", Dimension.LENGTH, Fraction(1))
km = BaseUnit("km", Dimension.LENGTH, Fraction(1000))
cd = BaseUnit("cd", Dimension.LUMINOUS_INTENSITY, Fraction(1))
ms = BaseUnit("ms", Dimension.TIME, Fraction(1, 1000))
s = BaseUnit("s", Dimension.TIME, Fraction(1))
mA = BaseUnit("mA", Dimension.ELECTRIC_CURRENT, Fraction(1, 1000))
A = BaseUnit("A", Dimension.ELECTRIC_CURRENT, Fraction(1))
K = BaseUnit("K", Dimension.TEMPERATURE, Fraction(1))
mol = BaseUnit("mol", Dimension.AMOUNT_OF_SUBSTANCE, Fraction(1))

lbs = BaseUnit("lbs", Dimension.MASS, Fraction(45359237, 100000000))
oz = BaseUnit("oz", Dimension.MASS, Fraction(45359237, 16*100000000))
inches = BaseUnit("in", Dimension.LENGTH, Fraction(381, 12*1250))
ft = BaseUnit("ft", Dimension.LENGTH, Fraction(381, 1250))

si_units = {
    Dimension.MASS: kg,
    Dimension.LENGTH: m,
    Dimension.LUMINOUS_INTENSITY: cd,
    Dimension.TIME: s,
    Dimension.ELECTRIC_CURRENT: A,
    Dimension.TEMPERATURE: K,
    Dimension.AMOUNT_OF_SUBSTANCE: mol,
}
