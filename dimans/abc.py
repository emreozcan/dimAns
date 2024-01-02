from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .dimension import Dimension, Dimensions
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
    # endregion


class Unit(Dimensional, ABC):
    symbol: str | None
    factor: Fraction | float

    def conversion_factor_to(self, other: Unit, /):
        """Get the conversion factor from this unit to another unit.

        This method returns the factor
        by which a measurement in this unit must be multiplied
        to get a measurement in the other unit.
        """
        if self.dimension_map() != other.dimension_map():
            raise ValueError(f"units must have the same dimensions")
        return self.si_factor() / other.si_factor()

    def conversion_factor_from(self, other: Unit, /):
        """Get the conversion factor from another unit to this unit.

        This method returns the factor
        by which a measurement in the other unit must be multiplied
        to get a measurement in this unit.
        """
        if self.dimension_map() != other.dimension_map():
            raise ValueError(f"units must have the same dimensions")
        return other.si_factor() / self.si_factor()

    @abstractmethod
    def as_derived_unit(self, symbol: str | None = None) -> DerivedUnit:
        pass

    @abstractmethod
    def as_quantity(self) -> Quantity:
        pass

    @classmethod
    @abstractmethod
    def using(
        cls,
        ref: Self, /, symbol: str | None = None, factor: Fraction | float = 1
    ) -> Self:
        pass

    @abstractmethod
    def si_factor(self) -> Fraction | float:
        pass

    @abstractmethod
    def multiplicative_inverse(self) -> DerivedUnit:
        pass


__all__ = [
    "Dimensional",
    "Unit",
]
