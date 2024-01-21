from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction
from functools import total_ordering
from typing import Self, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .dimension import Dimensions
    from . import DerivedUnit, Quantity


class Dimensional(ABC):
    @abstractmethod
    def dimensions(self) -> Dimensions:
        pass

    @abstractmethod
    def multiplicative_inverse(self) -> Self:
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
    def __pow__(self, power, modulo=None):
        pass

    # region Square root by pow
    def sqrt(self) -> Self:
        return self ** Fraction(1, 2)
    # endregion


@total_ordering
class Unit(Dimensional, ABC):
    def conversion_parameters_to(self, other: Unit, /) \
            -> tuple[Fraction | float, Fraction | float]:
        """Get the conversion parameters from this unit to another unit.

        A measurement in terms of this unit must be multiplied with the first
        element of the returned tuple,
        and the second element must be added
        to get a measurement in the other unit.
        """
        if self.dimensions() != other.dimensions():
            raise ValueError(f"units must have the same dimensions")

        from_factor, to_factor = self.si_factor(), other.si_factor()
        from_offset, to_offset = self.si_offset(), other.si_offset()

        if to_offset == 0 and from_offset == 0:
            return from_factor / to_factor, 0

        factor = from_factor / to_factor
        return factor, (from_offset * from_factor / to_factor - to_offset)

    def conversion_parameters_from(self, other: Unit, /) \
            -> tuple[Fraction | float, Fraction | float]:
        """Get the conversion parameters from another unit to this unit.

        A measurement in terms of the other unit must be multiplied with
        the first element of the returned tuple,
        and the second element must be added
        to get a measurement in this unit.
        """
        return other.conversion_parameters_to(self)

    @abstractmethod
    def as_derived_unit(self, symbol: str | None = None) -> DerivedUnit:
        pass

    @abstractmethod
    def as_quantity(self) -> Quantity:
        pass

    @abstractmethod
    def si_factor(self) -> Fraction | float:
        pass

    @abstractmethod
    def si_offset(self) -> Fraction | float:
        pass

    @abstractmethod
    def multiplicative_inverse(self) -> DerivedUnit:
        pass

    # region Comparison handlers
    def __eq__(self, other: Any, /):
        if not isinstance(other, Unit):
            return NotImplemented

        if self.dimensions() != other.dimensions():
            return False
        if self.si_factor() != other.si_factor():
            return False
        return True

    def __gt__(self, other: Any, /):
        if not isinstance(other, Unit):
            return NotImplemented

        if self.dimensions() != other.dimensions():
            raise ValueError(f"units must have the same dimensions")

        return self.si_factor() > other.si_factor()

    # endregion

    def __hash__(self):
        dim = self.dimensions()
        return hash((self.si_factor(), len(dim), sum(dim.values())))

    @abstractmethod
    def __add__(self, other) -> Unit:
        pass

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    # These arithmetic operations are redefined
    # from Dimensional for stricter typing.
    @abstractmethod
    def __mul__(self, other) -> Unit | Quantity:
        pass

    def __rmul__(self, other):
        return self.__mul__(other)

    @abstractmethod
    def __pow__(self, power: int | Fraction | float, modulo=None) -> Unit:
        pass


__all__ = [
    "Dimensional",
    "Unit",
]
