from __future__ import annotations

from abc import ABC, abstractmethod
from functools import total_ordering
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from .dimension import Dimensions
    from . import DerivedUnit, Quantity
    from fractions import Fraction


class Dimensional(ABC):
    @abstractmethod
    def dimensions(self) -> Dimensions:
        pass

    @abstractmethod
    def multiplicative_inverse(self) -> Dimensional:
        pass

    # region Arithmetic operations
    @abstractmethod
    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        return self.__mul__(other)

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __rtruediv__(self, other):
        pass

    @abstractmethod
    def __pow__(self, power: Fraction | int, modulo=None):
        pass

    # endregion


@total_ordering
class Unit(Dimensional, ABC):
    symbol: str | None

    def conversion_parameters_to(self, other: Unit, /) -> tuple[float, float]:
        """Get the conversion parameters from this unit to another unit.

        A measurement in terms of this unit must be multiplied with the first
        element of the returned tuple,
        and the second element must be added
        to get a measurement in the other unit.
        """
        if self.dimensions() != other.dimensions():
            raise ValueError("units must have the same dimensions")

        from_factor, to_factor = self.si_factor(), other.si_factor()
        from_offset, to_offset = self.si_offset(), other.si_offset()

        if to_offset == 0 and from_offset == 0:
            return from_factor / to_factor, 0

        factor = from_factor / to_factor
        return factor, (from_offset * from_factor / to_factor - to_offset)

    @abstractmethod
    def as_derived_unit(self, symbol: str | None = None) -> DerivedUnit:
        pass

    @abstractmethod
    def as_quantity(self) -> Quantity:
        pass

    @abstractmethod
    def si_factor(self) -> float | int:
        pass

    @abstractmethod
    def si_offset(self) -> float | int:
        pass

    @abstractmethod
    def with_symbol(self, symbol: str) -> Unit:
        pass

    @abstractmethod
    def multiplicative_inverse(self) -> DerivedUnit:
        pass

    # region Comparison handlers
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, Unit):
            return NotImplemented

        if self.dimensions() != other.dimensions():
            return False
        if self.si_factor() != other.si_factor():
            return False
        return True

    def __gt__(self, other: object, /) -> bool:
        if not isinstance(other, Unit):
            return NotImplemented

        if self.dimensions() != other.dimensions():
            raise ValueError("units must have the same dimensions")

        return self.si_factor() > other.si_factor()

    # endregion

    def __hash__(self) -> int:
        dim = self.dimensions()
        return hash((self.si_factor(), len(dim), sum(dim.values())))

    @abstractmethod
    def __add__(self, other: int | float) -> Unit:
        pass

    def __radd__(self, other: int | float) -> Unit:
        return self.__add__(other)

    def __sub__(self, other: int | float) -> Unit:
        return self.__add__(-other)

    # These arithmetic operations are redefined
    # from Dimensional for stricter typing.
    @overload
    def __mul__(self, other: Unit) -> DerivedUnit: ...

    @overload
    def __mul__(self, other: float | int) -> Quantity: ...

    @abstractmethod
    def __mul__(self, other):
        pass

    @overload
    def __rmul__(self, other: Unit) -> DerivedUnit: ...

    @overload
    def __rmul__(self, other: float | int) -> Quantity: ...

    def __rmul__(self, other):
        return self.__mul__(other)

    @abstractmethod
    def __pow__(self, power: Fraction | int, modulo=None) -> DerivedUnit:
        pass


__all__ = [
    "Dimensional",
    "Unit",
]
