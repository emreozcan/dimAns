from fractions import Fraction

import pytest

from dimans import BaseUnit, DerivedUnit, Quantity
from dimans.dimension import Dimension


dim_1 = Dimension("dim_1", "dim_1")


def test_baseunit_conversion_parameters():
    one = BaseUnit("1", dim_1, 1)
    two = BaseUnit("2", dim_1, 2)

    assert one.conversion_parameters_to(two) == (Fraction(1, 2), 0)
    assert two.conversion_parameters_to(one) == (2, 0)

    assert one.conversion_parameters_to(one) == (1, 0)


def test_baseunit_order():
    one = BaseUnit("1", dim_1, 1)
    two = BaseUnit("2", dim_1, 2)

    another_one = BaseUnit("1", dim_1, 1)

    assert one == another_one
    assert two != another_one
    assert one != two

    assert one < two
    assert two > one

    assert one <= two
    assert two >= one

    assert one <= one
    assert one >= one

    assert not (one > two)
    assert not (two < one)

    assert not (one > one)
    assert not (one < one)

    dim_2 = Dimension("dim_2", "dim_2")
    unrelated_unit = BaseUnit("unrelated", dim_2, 1)
    assert dim_1 != unrelated_unit


def test_baseunit_compare_other_dimensions():
    unit_1 = BaseUnit("1", dim_1, 1)

    dim_2 = Dimension("dim_2", "dim_2")
    unit_2 = BaseUnit("2", dim_2, 1)

    assert dim_1 != dim_2

    with pytest.raises(TypeError):
        assert unit_1 > 1

    with pytest.raises(ValueError):
        assert unit_1 > unit_2


def test_baseunit_dimensions():
    one = BaseUnit("1", dim_1, 1)
    dims = one.dimensions()

    assert len(dims) == 1
    assert dims[dim_1] == 1


def test_baseunit_conversion_to_derived_unit():
    one = BaseUnit("1", dim_1, 1)
    two = BaseUnit("2", dim_1, 2)

    one_du = one.as_derived_unit()
    two_du = two.as_derived_unit()

    assert one_du.conversion_parameters_to(two_du) == (Fraction(1, 2), 0)
    assert two_du.conversion_parameters_to(one_du) == (2, 0)

    assert one_du.conversion_parameters_to(one_du) == (1, 0)

    one_du_dims = one_du.dimensions()
    assert len(one_du_dims) == 1
    assert one_du_dims[dim_1] == 1

    assert one_du.dimensions() == two_du.dimensions()
    assert one_du.dimensions() == one.dimensions()

    assert one_du.si_factor() == one.si_factor()
    assert one_du.si_offset() == one.si_offset()

    assert two_du.si_factor() == two.si_factor()
    assert two_du.si_offset() == two.si_offset()


def test_baseunit_pow():
    two = BaseUnit("2", dim_1, 2)

    four = two ** Fraction(2)

    four_dims = four.dimensions()
    assert len(four_dims) == 1
    assert four_dims[dim_1] == 2

    assert four ** Fraction(1, 2) == two

    with pytest.raises(TypeError):
        assert two**two

    with pytest.raises(TypeError):
        assert two ** two.as_derived_unit()

    with pytest.raises(TypeError):
        assert two ** two.as_quantity()

    with pytest.raises(TypeError):
        assert two**1j


def test_baseunit_mul():
    base_unit = BaseUnit("x", dim_1, 2)
    other_base_unit = BaseUnit("y", dim_1, 3)
    derived_unit = base_unit.as_derived_unit()

    assert type(base_unit * base_unit) is DerivedUnit
    assert type(base_unit * derived_unit) is DerivedUnit
    assert type(base_unit * 1) is Quantity

    complicated_mul = base_unit * other_base_unit
    assert type(complicated_mul) is DerivedUnit
    assert len(complicated_mul.unit_exponents) == 2
    assert complicated_mul.unit_exponents[base_unit] == 1
    assert complicated_mul.unit_exponents[other_base_unit] == 1
    assert complicated_mul.si_factor() == 6

    quantity = other_base_unit.as_quantity()
    assert base_unit.__mul__(quantity) == NotImplemented

    assert base_unit * base_unit == base_unit ** Fraction(2)


def test_baseunit_div():
    some_unit = BaseUnit("x", dim_1, 16)
    some_other_unit = BaseUnit("y", dim_1, 4)

    assert some_unit / 1 is some_unit
    assert 1 / some_unit == some_unit.multiplicative_inverse()

    two_over_some_unit = 2 / some_unit
    assert two_over_some_unit == some_unit.multiplicative_inverse() * 2
    assert type(two_over_some_unit) is Quantity
    assert two_over_some_unit.unit == some_unit.multiplicative_inverse()
    assert two_over_some_unit.value == 2

    quotient = some_unit / some_other_unit
    assert type(quotient) is DerivedUnit
    assert len(quotient.unit_exponents) == 2
    assert quotient.unit_exponents[some_unit] == 1
    assert quotient.unit_exponents[some_other_unit] == -1

    with pytest.raises(TypeError):
        assert some_unit / 4


def test_baseunit_add():
    some_unit = BaseUnit("x", dim_1, 1)
    offset_unit = some_unit + 32

    assert type(offset_unit) is DerivedUnit
    assert len(offset_unit.unit_exponents) == 1
    assert offset_unit.unit_exponents[some_unit] == 1
    assert offset_unit.si_factor() == some_unit.si_factor()
    assert offset_unit.si_offset() == some_unit.si_offset() + 32

    assert offset_unit.conversion_parameters_to(some_unit) == (1, 32)

    with pytest.raises(TypeError):
        assert some_unit + some_unit

    with pytest.raises(TypeError):
        assert some_unit + some_unit.as_derived_unit()

    with pytest.raises(TypeError):
        assert some_unit + some_unit.as_quantity()


def test_baseunit_using():
    one = BaseUnit("1", dim_1, 1)
    two = BaseUnit("2", dim_1, 2)

    assert BaseUnit.using(one, factor=2, symbol="two times one") == two


def test_baseunit_multiplicative_inverse():
    two = BaseUnit("2", dim_1, 2)

    one_over_two = two.multiplicative_inverse()

    assert one_over_two == two ** Fraction(-1)
    assert type(one_over_two) is DerivedUnit
    assert len(one_over_two.unit_exponents) == 1
    assert one_over_two.unit_exponents[two] == -1

    one_over_two_dims = one_over_two.dimensions()
    assert len(one_over_two_dims) == 1
    assert one_over_two_dims[dim_1] == -1


def test_baseunit_as():
    some_unit = BaseUnit("x", dim_1, 1)

    derived_unit = some_unit.as_derived_unit()
    assert type(derived_unit) is DerivedUnit
    assert derived_unit.si_factor() == some_unit.si_factor()
    assert derived_unit.si_offset() == some_unit.si_offset()

    quantity = some_unit.as_quantity()
    assert type(quantity) is Quantity
    assert quantity.unit == some_unit
    assert quantity.value == 1


def test_baseunit_repr():
    assert repr(BaseUnit("x", dim_1, 1)) == "<BaseUnit x>"
    assert repr(BaseUnit("x", dim_1, 2)) == "<BaseUnit x>"


def test_baseunit_str():
    assert str(BaseUnit("x", dim_1, 1)) == "x"
    assert str(BaseUnit("x", dim_1, 2)) == "x"
