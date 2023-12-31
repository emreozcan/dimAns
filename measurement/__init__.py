from __future__ import annotations as _annotations

from collections.abc import Mapping as _Mapping
from enum import Enum as _Enum
from fractions import Fraction as _Fraction
from functools import total_ordering as _total_ordering
from numbers import Rational as _Rational, Real as _Real
from typing import Any as _Any

import attrs as _attrs


@_total_ordering
@_attrs.define(slots=True, frozen=True, repr=False, eq=False)
class Quantity:
    value: _Real
    unit: DerivedUnit

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | _Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, _Rational):
                return NotImplemented
            power = _Fraction(power)
        if not isinstance(self.value, float):
            if not isinstance(self.value, _Rational):
                return NotImplemented
            value = _Fraction(self.value)
        else:
            value = self.value
        return Quantity(value ** power, self.unit ** power)

    def __mul__(self, other: _Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit * other.unit
            if not new_unit.dimension_map():
                return self.value * other.value * new_unit.factor
            return Quantity(self.value * other.value, new_unit)
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return self * other.as_quantity()
        if isinstance(other, _Real):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    __rmul__ = __mul__

    def __add__(self, other: _Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                raise ValueError(f"units must be the same")
            return Quantity(self.value + other.value, self.unit)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: _Any, /):
        if isinstance(other, Quantity):
            return self + other.additive_inverse()
        return NotImplemented

    def __rsub__(self, other: _Any, /):
        return other + self.additive_inverse()

    def __abs__(self):
        return Quantity(abs(self.value), self.unit)

    def __ceil__(self):
        return Quantity(self.value.__ceil__(), self.unit)

    def __floor__(self):
        return Quantity(self.value.__floor__(), self.unit)

    def __truediv__(self, other: _Any, /):
        if isinstance(other, Quantity):
            return self * other.multiplicative_inverse()
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return self / other.as_quantity()
        if isinstance(other, _Real):
            return Quantity(self.value / other, self.unit)
        return NotImplemented

    def __rtruediv__(self, other: _Any, /):
        if isinstance(other, Quantity):
            return self.multiplicative_inverse() * other
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return self.multiplicative_inverse() * other.as_quantity()
        if isinstance(other, _Real):
            return Quantity(
                other / self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __divmod__(self, other: _Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                #       Please note that dividing a Quantity by a Quantity
                #       may result in a regular Integral.
                raise ValueError(f"units must be the same")
            div_, mod_ = divmod(self.value, other.value)
            return div_, Quantity(mod_, self.unit)
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return divmod(self, other.as_quantity())
        return NotImplemented

    def __floordiv__(self, other: _Any, /):
        if isinstance(other, Quantity):
            new_unit = self.unit / other.unit
            if not new_unit.dimension_map():
                return self.value // other.value * new_unit.factor
            return Quantity(self.value // other.value, new_unit)
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return self // other.as_quantity()
        if isinstance(other, _Real):
            return Quantity(self.value // other, self.unit)
        return NotImplemented

    def __rfloordiv__(self, other: _Any, /):
        if isinstance(other, Quantity):
            new_unit = other.unit / self.unit
            if not new_unit.dimension_map():
                return other.value // self.value * new_unit.factor
            return Quantity(other.value // self.value, new_unit)
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return other.as_quantity() // self
        if isinstance(other, _Real):
            return Quantity(
                other // self.value,
                self.unit.multiplicative_inverse()
            )
        return NotImplemented

    def __mod__(self, other: _Any, /):
        if isinstance(other, Quantity):
            if self.unit != other.unit:
                # todo: Remove this restriction.
                raise ValueError(f"units must be the same")
            return Quantity(self.value % other.value, self.unit)
        if isinstance(other, (DerivedUnit, BaseUnit)):
            return self % other.as_quantity()
        return NotImplemented

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __round__(self, n=None):
        return Quantity(self.value.__round__(n), self.unit)
    # endregion

    # region Comparison handlers
    def __eq__(self, other: _Any, /):
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

    def convert_to(self, other: DerivedUnit | BaseUnit, /):
        """Convert this quantity to another unit.

        This method returns a new Quantity
        which is equivalent to this quantity
        but in the other unit.
        """
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if self.unit.dimensions() != other.dimensions():
            raise ValueError(f"target unit must have the same dimensions")
        return Quantity(
            self.value * self.unit.conversion_factor_to(other),
            other
        )

    def as_unit(self, symbol: str = None) -> DerivedUnit:
        return DerivedUnit(
            symbol,
            self.unit.unit_exponents,
            self.unit.factor * self.value
        )


@_total_ordering
@_attrs.define(slots=True, frozen=True, repr=False, eq=False)
class DerivedUnit:
    """Represents a product of one or more base units."""
    symbol: str | None
    unit_exponents: _Mapping[BaseUnit, _Fraction | float]
    factor: _Fraction = _Fraction(1)

    @classmethod
    def named(
        cls,
        symbol: str,
        exponents_or_unit: _Mapping[BaseUnit, _Fraction | float] | DerivedUnit,
        /
    ):
        if isinstance(exponents_or_unit, DerivedUnit):
            return cls(
                symbol,
                exponents_or_unit.unit_exponents,
                exponents_or_unit.factor
            )
        return cls(symbol, exponents_or_unit)

    @classmethod
    def using(
        cls,
        ref: DerivedUnit,
        symbol: str | None,
        factor: _Fraction = _Fraction(1),
    ):
        return cls(symbol, ref.unit_exponents, ref.factor * factor)

    def __str__(self):
        if self.symbol:
            return self.symbol
        if self.factor == 1:
            return self._str_with_multiplicands()
        return f"{self.factor} {self._str_with_multiplicands()}"

    def __repr__(self):
        if self.symbol:
            if self.factor != 1:
                return (f"<{self.__class__.__name__} {self} "
                        f"= {self.factor} {self._str_with_multiplicands()}>")
            return (f"<{self.__class__.__name__} {self} "
                    f"= {self._str_with_multiplicands()}>")
        if self.factor != 1:
            return f"<{self.__class__.__name__} {self.factor} {self}>"
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | _Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, _Rational):
                return NotImplemented
            power = _Fraction(power)
        return DerivedUnit(
            None,
            {
                base_unit: exponent * power
                for base_unit, exponent in self.unit_exponents.items()
            },
            # For some reason, my type checker thinks Fraction ** int is float.
            self.factor ** power  # type: ignore
        )

    def __mul__(self, other: _Any, /):
        if isinstance(other, DerivedUnit):
            base_units = []
            for unit in self.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)
            for unit in other.unit_exponents.keys():
                if unit not in base_units:
                    base_units.append(unit)

            return DerivedUnit(
                None,
                {
                    base_unit: exponent
                    for base_unit, exponent in {
                        base_unit:
                            self.unit_exponents.get(base_unit, 0) +
                            other.unit_exponents.get(base_unit, 0)
                        for base_unit in base_units
                    }.items()
                    if exponent != 0
                },
                self.factor * other.factor
            )

        if isinstance(other, _Real):
            return Quantity(other, self)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: _Any, /):
        if other == 1:
            return self
        if isinstance(other, DerivedUnit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: _Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    # region Comparison handlers
    def __eq__(self, other: _Any, /):
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if isinstance(other, DerivedUnit):
            if self.dimension_map() != other.dimension_map():
                return False
            if self.si_factor() != other.si_factor():
                return False
            return True
        return NotImplemented

    def __gt__(self, other: _Any, /):
        if isinstance(other, BaseUnit):
            other = other.as_unit()
        if isinstance(other, DerivedUnit):
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
        factor = self.factor
        for base_unit, exponent in self.unit_exponents.items():
            factor *= base_unit.si_factor ** exponent
        return factor

    def conversion_factor_to(self, other: DerivedUnit | BaseUnit, /):
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

    def conversion_factor_from(self, other: DerivedUnit | BaseUnit, /):
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

    def as_unit(self, symbol: str = None) -> DerivedUnit:
        return DerivedUnit.named(symbol, self)

    def multiplicative_inverse(self):
        return DerivedUnit(
            None,
            {
                base_unit: -exponent
                for base_unit, exponent in self.unit_exponents.items()
            },
            1 / self.factor
        )


@_total_ordering
@_attrs.define(slots=True, frozen=True, repr=False, eq=False, hash=True)
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

    si_factor: _Fraction
    """The factor by which the base SI unit of the dimension is multiplied by.
    """

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    # region Arithmetic operation handlers
    def __pow__(self, power: int | _Fraction | float, modulo=None):
        if not isinstance(power, float):
            if not isinstance(power, _Rational):
                return NotImplemented
            power = _Fraction(power)
        return DerivedUnit(None, {self: power})

    def __mul__(self, other: _Any, /):
        if isinstance(other, DerivedUnit):
            return self.as_unit() * other

        if isinstance(other, BaseUnit):
            if self == other:
                return self ** 2
            return self.as_unit() * other.as_unit()

        if isinstance(other, _Real):
            return Quantity(other, self.as_unit())
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: _Any, /):
        if other == 1:
            return self
        if isinstance(other, BaseUnit):
            return self * other.multiplicative_inverse()
        return NotImplemented

    def __rtruediv__(self, other: _Any, /):
        if other == 1:
            return self.multiplicative_inverse()
        return other * self.multiplicative_inverse()
    # endregion

    # region Comparison handlers
    def __eq__(self, other: _Any, /):
        if isinstance(other, DerivedUnit):
            return self.as_unit() == other
        if isinstance(other, BaseUnit):
            if self.dimension != other.dimension:
                return False
            if self.si_factor != other.si_factor:
                return False
            return True
        return NotImplemented

    def __gt__(self, other: _Any, /):
        if isinstance(other, DerivedUnit):
            return self.as_unit() > other
        if isinstance(other, BaseUnit):
            if self.dimension != other.dimension:
                raise ValueError(f"units must have the same dimensions")
            return self.si_factor > other.si_factor
        return NotImplemented
    # endregion

    def _check_compatible(self, other: _Any, /):
        if not isinstance(other, BaseUnit):
            raise TypeError(f"expected BaseUnit, "
                            f"got {other.__class__.__name__}")
        if self.dimension != other.dimension:
            raise ValueError(f"{self.dimension} unit not compatible with "
                             f"{other.dimension} unit")

    def dimension_map(self):
        return {self.dimension: _Fraction(1)}

    def dimensions(self):
        return Dimensions.from_map(self.dimension_map())

    def conversion_factor_to(self, other: BaseUnit | DerivedUnit, /):
        """Get the conversion factor from this unit to another unit.

        This method returns the factor
        by which a measurement in this unit must be multiplied
        to get a measurement in the other unit.
        """
        if isinstance(other, DerivedUnit):
            return self.as_unit().conversion_factor_to(other)
        self._check_compatible(other)
        return self.si_factor / other.si_factor

    def conversion_factor_from(self, other: BaseUnit | DerivedUnit, /):
        """Get the conversion factor from another unit to this unit.

        This method returns the factor
        by which a measurement in the other unit must be multiplied
        to get a measurement in this unit.
        """
        if isinstance(other, DerivedUnit):
            return self.as_unit().conversion_factor_from(other)
        self._check_compatible(other)
        return other.si_factor / self.si_factor

    def as_unit(self) -> DerivedUnit:
        return DerivedUnit(None, {self: 1})

    def as_quantity(self) -> Quantity:
        return Quantity(1, self.as_unit())

    def multiplicative_inverse(self) -> DerivedUnit:
        return DerivedUnit(None, {self: -1})

    @classmethod
    def using(cls, ref: BaseUnit, symbol: str, factor: _Fraction):
        return cls(symbol, ref.dimension, ref.si_factor * factor)


@_attrs.define(slots=True, frozen=True, repr=False)
class Dimensions:
    mass: _Fraction | float = _Fraction(0)
    length: _Fraction | float = _Fraction(0)
    luminous_intensity: _Fraction | float = _Fraction(0)
    time: _Fraction | float = _Fraction(0)
    electric_current: _Fraction | float = _Fraction(0)
    temperature: _Fraction | float = _Fraction(0)
    amount_of_substance: _Fraction | float = _Fraction(0)

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
    def from_map(cls, _map: _Mapping[Dimension, _Fraction | float]):
        return cls(
            _map.get(Dimension.MASS, _Fraction(0)),
            _map.get(Dimension.LENGTH, _Fraction(0)),
            _map.get(Dimension.LUMINOUS_INTENSITY, _Fraction(0)),
            _map.get(Dimension.TIME, _Fraction(0)),
            _map.get(Dimension.ELECTRIC_CURRENT, _Fraction(0)),
            _map.get(Dimension.TEMPERATURE, _Fraction(0)),
            _map.get(Dimension.AMOUNT_OF_SUBSTANCE, _Fraction(0)),
        )

    def as_map(self) -> _Mapping[Dimension, _Fraction | float]:
        return {
            Dimension.MASS: self.mass,
            Dimension.LENGTH: self.length,
            Dimension.LUMINOUS_INTENSITY: self.luminous_intensity,
            Dimension.TIME: self.time,
            Dimension.ELECTRIC_CURRENT: self.electric_current,
            Dimension.TEMPERATURE: self.temperature,
            Dimension.AMOUNT_OF_SUBSTANCE: self.amount_of_substance,
        }


class Dimension(_Enum):
    MASS = "M"
    LENGTH = "L"
    LUMINOUS_INTENSITY = "J"
    TIME = "T"
    ELECTRIC_CURRENT = "I"
    TEMPERATURE = "Θ"
    AMOUNT_OF_SUBSTANCE = "N"
