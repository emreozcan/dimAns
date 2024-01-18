from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Self, TYPE_CHECKING

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

    @abstractmethod
    def __rmul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __rtruediv__(self, other):
        pass

    @abstractmethod
    def __pow__(self, power, modulo=None):
        pass

    @abstractmethod
    def sqrt(self) -> Self:
        pass
    # endregion


class Unit(Dimensional, ABC):
    symbol: str | None
    factor: Fraction | float

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


__all__ = [
    "Dimensional",
    "Unit",
]
