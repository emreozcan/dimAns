from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from fractions import Fraction
from functools import total_ordering
from numbers import Rational, Real
from typing import Any

import attrs


@total_ordering
@attrs.define(slots=True, frozen=True, repr=False, eq=False)
class Quantity:
    value: Real
    unit: CompoundUnit

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, Rational):
                return NotImplemented
            power = Fraction(power)
        if not isinstance(self.value, float):
            if not isinstance(self.value, Rational):
                return NotImplemented
            value = Fraction(self.value)
        else:
            value = self.value
        return Quantity(value ** power, self.unit ** power)

    def __mul__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit * other.unit
            if not new_unit.dimension_map():
                return self.value * other.value
            return Quantity(self.value * other.value, new_unit)
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return self * other.as_quantity()
        if isinstance(other, Real):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    __rmul__ = __mul__

    def __add__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                raise ValueError(f"units must be the same")
            return Quantity(self.value + other.value, self.unit)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self + other.additive_inverse()
        return NotImplemented

    def __rsub__(self, other: Any, /):
        return other + self.additive_inverse()

    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __ceil__(self):
        return Quantity(self.value.__ceil__(), self.unit)

    def __floor__(self):
        return Quantity(self.value.__floor__(), self.unit)

    def __truediv__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self * other.multiplicative_inverse()
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return self / other.as_quantity()
        if isinstance(other, Real):
            return Quantity(self.value / other, self.unit)
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if isinstance(other, Quantity):
            return self.multiplicative_inverse() * other
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return self.multiplicative_inverse() * other.as_quantity()
        if isinstance(other, Real):
            return Quantity(
                other / self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __divmod__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                #       Please note that dividing a Quantity by a Quantity
                #       may result in a regular Integral.
                raise ValueError(f"units must be the same")
            div_, mod_ = divmod(self.value, other.value)
            return div_, Quantity(mod_, self.unit)
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return divmod(self, other.as_quantity())
        return NotImplemented

    def __floordiv__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit / other.unit
            if not new_unit.dimension_map():
                return self.value // other.value
            return Quantity(self.value // other.value, new_unit)
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return self // other.as_quantity()
        if isinstance(other, Real):
            return Quantity(self.value // other, self.unit)
        return NotImplemented

    def __rfloordiv__(self, other: Any, /):
        if isinstance(other, Quantity):
            new_unit = other.unit / self.unit
            if not new_unit.dimension_map():
                return other.value // self.value
            return Quantity(other.value // self.value, new_unit)
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return other.as_quantity() // self
        if isinstance(other, Real):
            return Quantity(
                other // self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __mod__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                raise ValueError(f"units must be the same")
            return Quantity(self.value % other.value, self.unit)
        if isinstance(other, (CompoundUnit, BaseUnit)):
            return self % other.as_quantity()
        return NotImplemented

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __round__(self, n=None):
        return Quantity(self.value.__round__(n), self.unit)
    # endregion

    # region Comparison handlers
    def __eq__(self, other: Any, /):
        if isinstance(other, Quantity):
            if self.dimension_map() != other.dimension_map():
                return False
            if (self.value * self.unit.si_factor()
                    != other.value * other.unit.si_factor()):
                return False
            return True
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Quantity):
            if self.dimension_map() != other.dimension_map():
                raise ValueError(f"units must have the same dimensions")
            return (self.value * self.unit.si_factor()
                    > other.value * other.unit.si_factor())
        return NotImplemented
    # endregion

    def dimension_map(self):
        return self.unit.dimension_map()

    def dimensions(self):
        return self.unit.dimensions()

    def multiplicative_inverse(self):
        return Quantity(1 / self.value, self.unit.multiplicative_inverse())

    def additive_inverse(self):
        return Quantity(-self.value, self.unit)

    def convert_to(self, other: CompoundUnit | BaseUnit, /):
        """Convert this quantity to another unit.

        This method returns a new Quantity
        which is equivalent to this quantity
        but in the other unit.
        """
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if self.unit.dimensions() != other.dimensions():
            raise ValueError(f"target unit must have the same dimensions")
        return self * self.unit.conversion_factor_to(other)


@total_ordering
@attrs.define(slots=True, frozen=True, repr=False, eq=False)
class CompoundUnit:
    """Represents a product of one or more base units."""
    symbol: str | None
    unit_exponents: Mapping[BaseUnit, Fraction | float]

    @classmethod
    def named(
        cls,
        symbol: str,
        exponents_or_unit: Mapping[BaseUnit, Fraction | float] | CompoundUnit,
        /
    ):
        if isinstance(exponents_or_unit, CompoundUnit):
            return cls(symbol, exponents_or_unit.unit_exponents)
        return cls(symbol, exponents_or_unit)

    def __str__(self):
        if self.symbol:
            return self.symbol
        return self._str_with_multiplicands()

    def __repr__(self):
        if self.symbol:
            return (f"<{self.__class__.__name__} {self} "
                    f"= {self._str_with_multiplicands()}>")
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, Rational):
                return NotImplemented
            power = Fraction(power)
        return CompoundUnit(None, {
            base_unit: exponent * power
            for base_unit, exponent in self.unit_exponents.items()
        })

    def __mul__(self, other: Any, /):
        if isinstance(other, CompoundUnit):
            base_units = []
            for unit in self.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)
            for unit in other.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)

            return CompoundUnit(None, {
                base_unit: exponent
                for base_unit, exponent in {
                    base_unit:
                        self.unit_exponents.get(base_unit, 0) +
                        other.unit_exponents.get(base_unit, 0)
                    for base_unit in base_units
                }.items()
                if exponent != 0
            })

        if isinstance(other, Real):
            return Quantity(other, self)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Any, /):
        if other == 1:
            return self
        if isinstance(other, CompoundUnit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    # region Comparison handlers
    def __eq__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if isinstance(other, CompoundUnit):
            if self.dimension_map() != other.dimension_map():
                return False
            if self.si_factor() != other.si_factor():
                return False
            return True
        return NotImplemented

    def __gt__(self, other: Any, /):
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if isinstance(other, CompoundUnit):
            if self.dimension_map() != other.dimension_map():
                raise ValueError(f"units must have the same dimensions")
            return self.si_factor() > other.si_factor()
        return NotImplemented
    # endregion

    def _str_with_multiplicands(self):
        if not self.unit_exponents:
            return "1"
        return " ".join([
            f"{base_unit}^{exponent}" if exponent != 1 else str(base_unit)
            for base_unit, exponent in self.unit_exponents.items()
        ])

    def dimension_map(self):
        dimensions = {}
        for base_unit, exponent in self.unit_exponents.items():
            if base_unit.dimension not in dimensions:
                dimensions[base_unit.dimension] = exponent
            else:
                dimensions[base_unit.dimension] += exponent
                if dimensions[base_unit.dimension] == 0:
                    del dimensions[base_unit.dimension]
        return dimensions

    def dimensions(self):
        return Dimensions.from_map(self.dimension_map())

    def si_factor(self):
        factor = 1
        for base_unit, exponent in self.unit_exponents.items():
            factor *= base_unit.si_factor ** exponent
        return factor

    def conversion_factor_to(self, other: CompoundUnit | BaseUnit, /):
        """Get the conversion factor from this unit to another unit.

        This method returns the factor
        by which a measurement in this unit must be multiplied
        to get a measurement in the other unit.
        """
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if self.dimensions() != other.dimensions():
            raise ValueError(f"units must have the same dimensions")
        return self.si_factor() / other.si_factor()

    def conversion_factor_from(self, other: CompoundUnit | BaseUnit, /):
        """Get the conversion factor from another unit to this unit.

        This method returns the factor
        by which a measurement in the other unit must be multiplied
        to get a measurement in this unit.
        """
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if self.dimensions() != other.dimensions():
            raise ValueError(f"units must have the same dimensions")
        return other.si_factor() / self.si_factor()

    def as_quantity(self) -> Quantity:
        return Quantity(1, self)

    def multiplicative_inverse(self):
        return CompoundUnit(None, {
            base_unit: -exponent
            for base_unit, exponent in self.unit_exponents.items()
        })


@total_ordering
@attrs.define(slots=True, frozen=True, repr=False, eq=False, hash=True)
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

    # region Arithmetic operation handlers
    def __pow__(self, power: int | Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, Rational):
                return NotImplemented
            power = Fraction(power)
        return CompoundUnit(None, {self: power})

    def __mul__(self, other: Any, /):
        if isinstance(other, CompoundUnit):
            return self.as_unit() * other

        if isinstance(other, BaseUnit):
            if self == other:
                return self ** 2
            return self.as_unit() * other.as_unit()

        if isinstance(other, Real):
            return Quantity(other, self.as_unit())
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Any, /):
        if other == 1:
            return self
        if isinstance(other, BaseUnit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    # region Comparison handlers
    def __eq__(self, other: Any, /):
        if isinstance(other, CompoundUnit):
            return self.as_unit() == other
        if isinstance(other, BaseUnit):
            if self.dimension != other.dimension:
                return False
            if self.si_factor != other.si_factor:
                return False
            return True
        return NotImplemented

    def __gt__(self, other: Any, /):
        if isinstance(other, CompoundUnit):
            return self.as_unit() > other
        if isinstance(other, BaseUnit):
            if self.dimension != other.dimension:
                raise ValueError(f"units must have the same dimensions")
            return self.si_factor > other.si_factor
        return NotImplemented
    # endregion

    def _check_compatible(self, other: Any, /):
        if not isinstance(other, BaseUnit):
            raise TypeError(f"expected BaseUnit, "
                            f"got {other.__class__.__name__}")
        if self.dimension != other.dimension:
            raise ValueError(f"{self.dimension} unit not compatible with "
                             f"{other.dimension} unit")

    def dimension_map(self):
        return {self.dimension: Fraction(1)}

    def dimensions(self):
        return Dimensions.from_map(self.dimension_map())

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

    def as_unit(self) -> CompoundUnit:
        return CompoundUnit(None, {self: 1})

    def as_quantity(self) -> Quantity:
        return Quantity(1, self.as_unit())

    def multiplicative_inverse(self) -> CompoundUnit:
        return CompoundUnit(None, {self: -1})

    @classmethod
    def using(cls, ref: BaseUnit, symbol: str, factor: Fraction):
        return cls(symbol, ref.dimension, ref.si_factor * factor)


@attrs.define(slots=True, frozen=True, repr=False)
class Dimensions:
    mass: Fraction | float = Fraction(0)
    length: Fraction | float = Fraction(0)
    luminous_intensity: Fraction | float = Fraction(0)
    time: Fraction | float = Fraction(0)
    electric_current: Fraction | float = Fraction(0)
    temperature: Fraction | float = Fraction(0)
    amount_of_substance: Fraction | float = Fraction(0)

    def __str__(self):
        if all(exponent == 0 for exponent in self.as_map().values()):
            return "1"

        return " ".join([
            f"{dimension.value}^{exponent}"
            for dimension, exponent in self.as_map().items()
            if exponent != 0
        ])

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    @classmethod
    def from_map(cls, _map: Mapping[Dimension, Fraction | float]):
        return cls(
            _map.get(Dimension.MASS, Fraction(0)),
            _map.get(Dimension.LENGTH, Fraction(0)),
            _map.get(Dimension.LUMINOUS_INTENSITY, Fraction(0)),
            _map.get(Dimension.TIME, Fraction(0)),
            _map.get(Dimension.ELECTRIC_CURRENT, Fraction(0)),
            _map.get(Dimension.TEMPERATURE, Fraction(0)),
            _map.get(Dimension.AMOUNT_OF_SUBSTANCE, Fraction(0)),
        )

    def as_map(self) -> Mapping[Dimension, Fraction | float]:
        return {
            Dimension.MASS: self.mass,
            Dimension.LENGTH: self.length,
            Dimension.LUMINOUS_INTENSITY: self.luminous_intensity,
            Dimension.TIME: self.time,
            Dimension.ELECTRIC_CURRENT: self.electric_current,
            Dimension.TEMPERATURE: self.temperature,
            Dimension.AMOUNT_OF_SUBSTANCE: self.amount_of_substance,
        }


class Dimension(Enum):
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
h = BaseUnit("h", Dimension.TIME, Fraction(3600))
mA = BaseUnit("mA", Dimension.ELECTRIC_CURRENT, Fraction(1, 1000))
A = BaseUnit("A", Dimension.ELECTRIC_CURRENT, Fraction(1))
K = BaseUnit("K", Dimension.TEMPERATURE, Fraction(1))
mol = BaseUnit("mol", Dimension.AMOUNT_OF_SUBSTANCE, Fraction(1))

lbs = BaseUnit("lbs", Dimension.MASS, Fraction(45359237, 100000000))
oz = BaseUnit("oz", Dimension.MASS, Fraction(45359237, 16*100000000))
inches = BaseUnit("in", Dimension.LENGTH, Fraction(381, 12*1250))
ft = BaseUnit("ft", Dimension.LENGTH, Fraction(381, 1250))
mi = BaseUnit("mi", Dimension.LENGTH, Fraction(201168, 125))

si_units = {
    Dimension.MASS: kg,
    Dimension.LENGTH: m,
    Dimension.LUMINOUS_INTENSITY: cd,
    Dimension.TIME: s,
    Dimension.ELECTRIC_CURRENT: A,
    Dimension.TEMPERATURE: K,
    Dimension.AMOUNT_OF_SUBSTANCE: mol,
}
