from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from fractions import Fraction
from numbers import Number, Rational
from typing import Any

import attrs


@attrs.define(slots=True, frozen=True, eq=False)
class Quantity:
    value: Number
    unit: Unit


@attrs.define(slots=True, frozen=True, eq=False)
class Unit:
    base_unit_exponents: Mapping[Dimension, BaseUnitExponent]


@attrs.define(slots=True, frozen=True, repr=False)
class BaseUnitExponent:
    """Represents a base unit raised to some exponent."""

    base_unit: BaseUnit
    exponent: Fraction | float

    def __str__(self):
        return f"{self.base_unit}^{self.exponent}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    def __pow__(self, power: int | Fraction | float, modulo=None):
        if isinstance(power, float):  # Do not touch floats
            return self.base_unit ** (self.exponent * power)
        # Convert everything except floats to Fraction
        if not isinstance(power, Rational):
            return NotImplemented
        return self.base_unit ** (self.exponent * Fraction(power))

    def __mul__(self, other: Any, /):
        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self.base_unit:
                return self.base_unit ** (self.exponent + other.exponent)
            return NotImplemented  # todo: implement this
        return NotImplemented

    def __rmul__(self, other: Any, /):
        return self * other  # Multiplication is commutative

    def __truediv__(self, other: Any, /):
        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self.base_unit:
                return self.base_unit ** (self.exponent - other.exponent)
            return NotImplemented  # todo: implement this
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self.base_unit:
                return self.base_unit ** (other.exponent - self.exponent)
            return NotImplemented  # todo: implement this
        return NotImplemented


@attrs.define(slots=True, frozen=True, repr=False)
class BaseUnit:
    """A unit of measurement which only has one dimension of power 1.

    What the above statement means in layman's terms is that
    a base unit is a unit, which is not a combination of other units.

    For example, the meter is a base unit, the second is a base unit, but
    meters per second is not a base unit.
    """

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
        return f"<{self.__class__.__name__} {self}>"

    def __pow__(self, power: int | Fraction | float, modulo=None):
        if isinstance(power, float):  # Do not touch floats
            return BaseUnitExponent(self, power)
        # Convert everything except floats to Fraction
        if not isinstance(power, Rational):
            return NotImplemented
        return BaseUnitExponent(self, Fraction(power))

    def __mul__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            if self == other:
                return self ** 2
            return NotImplemented  # todo: implement this

        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self:
                return self ** (other.exponent + 1)
            return NotImplemented  # todo: implement this

        if other == 1:
            return self
        return NotImplemented

    def __rmul__(self, other: Any, /):
        return self * other  # Multiplication is commutative

    def __truediv__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            if self == other:
                return 1
            return NotImplemented  # todo: implement this
        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self:
                return self ** (1 - other.exponent)
            return NotImplemented  # todo: implement this.
        if other == 1:
            return self
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            if self == other:
                return 1
            return NotImplemented  # todo: implement this
        if isinstance(other, BaseUnitExponent):
            if other.base_unit == self:
                return self ** (other.exponent - 1)
            return NotImplemented  # todo: implement this
        if other == 1:
            return self ** -1
        return NotImplemented

    def _check_compatible(self, other: Any, /):
        if not isinstance(other, BaseUnit):
            raise TypeError(f"expected BaseUnit, "
                            f"got {other.__class__.__name__}")
        if self.dimension != other.dimension:
            raise ValueError(f"{self.dimension} unit not compatible with "
                             f"{other.dimension} unit")

    def conversion_factor_to(self, other: BaseUnit, /):
        """Get the conversion factor from this unit to another unit.

        This method returns the factor
        by which a measurement in this unit must be multiplied
        to get a measurement in the other unit.
        """
        self._check_compatible(other)
        return self.si_factor / other.si_factor

    def conversion_factor_from(self, other: BaseUnit, /):
        """Get the conversion factor from another unit to this unit.

        This method returns the factor
        by which a measurement in the other unit must be multiplied
        to get a measurement in this unit.
        """
        self._check_compatible(other)
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

    def si_base_unit(self) -> BaseUnit | None:
        return si_units[self]


mg = BaseUnit("mg", Dimension.MASS, Fraction(1, 1_000_000))
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
    Dimension.ONE: None,
    Dimension.MASS: kg,
    Dimension.LENGTH: m,
    Dimension.LUMINOUS_INTENSITY: cd,
    Dimension.TIME: s,
    Dimension.ELECTRIC_CURRENT: A,
    Dimension.TEMPERATURE: K,
    Dimension.AMOUNT_OF_SUBSTANCE: mol,
}
