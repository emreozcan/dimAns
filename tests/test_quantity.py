from fractions import Fraction

import pytest

from dimans import BaseUnit, DerivedUnit, Quantity
from dimans.dimension import Dimension


dim_1 = Dimension("dim_1", "dim_1")

one = BaseUnit("one", dim_1, 1)
three = BaseUnit("three", dim_1, 3)
seven = BaseUnit("seven", dim_1, 7)
ten = BaseUnit("ten", dim_1, 10)


def test_conversion():
    assert (10 * one).to(ten) == (1 * ten)
