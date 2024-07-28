from fractions import Fraction

import pytest

from dimans import BaseUnit, DerivedUnit, Quantity
from dimans.dimension import Dimension, Dimensions


dim_1 = Dimension("dim_1", "dim_1")
dim_2 = Dimension("dim_2", "dim_2")

base_dim_1 = BaseUnit("base_dim_1", dim_1, 1)
base_dim_1_alt = BaseUnit("base_dim_1_alt", dim_1, 1)
base_dim_2 = BaseUnit("base_dim_2", dim_2, 1)

derived_complicated = DerivedUnit(
    symbol="derived_complicated",
    unit_exponents={
        base_dim_1: Fraction(1, 2),
        base_dim_2: Fraction(-1, 2),
    },
    factor=16,
    offset=9,
)


def test_derived_unit_str():
    assert str(derived_complicated) == "derived_complicated"

    assert (
        str(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=0,
            )
        )
        == "base_dim_1^3/2"
    )

    assert (
        str(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=12,
            )
        )
        == "base_dim_1^3/2 + 12"
    )

    assert (
        str(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=0,
            )
        )
        == "9 base_dim_1^3/2"
    )

    assert (
        str(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=6,
            )
        )
        == "9 base_dim_1^3/2 + 6"
    )


def test_derived_unit_repr():
    assert (
        repr(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=0,
            )
        )
        == "<DerivedUnit base_dim_1^3/2>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol="derived_1",
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=0,
            )
        )
        == "<DerivedUnit derived_1 = base_dim_1^3/2>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=12,
            )
        )
        == "<DerivedUnit base_dim_1^3/2 + 12>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol="derived_2",
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=1,
                offset=12,
            )
        )
        == "<DerivedUnit derived_2 = base_dim_1^3/2 + 12>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=0,
            )
        )
        == "<DerivedUnit 9 base_dim_1^3/2>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol="derived_3",
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=0,
            )
        )
        == "<DerivedUnit derived_3 = 9 base_dim_1^3/2>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol=None,
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=6,
            )
        )
        == "<DerivedUnit 9 base_dim_1^3/2 + 6>"
    )

    assert (
        repr(
            DerivedUnit(
                symbol="derived_4",
                unit_exponents={base_dim_1: Fraction(3, 2)},
                factor=9,
                offset=6,
            )
        )
        == "<DerivedUnit derived_4 = 9 base_dim_1^3/2 + 6>"
    )


def test_derived_unit_dimensionless_repr():
    assert (
        repr(
            DerivedUnit(
                symbol=None,
                unit_exponents={},
                factor=9,
                offset=6,
            )
        )
        == "<DerivedUnit 9 1 + 6>"
    )


def test_derived_unit_dimensions():
    assert derived_complicated.dimensions() == Dimensions(
        {
            dim_1: Fraction(1, 2),
            dim_2: Fraction(-1, 2),
        }
    )

    assert (
        DerivedUnit(
            symbol=None,
            unit_exponents={base_dim_1: Fraction(3, 2)},
        )
        * DerivedUnit(
            symbol=None,
            unit_exponents={base_dim_1_alt: Fraction(1, 2)},
        )
    ).dimensions() == Dimensions({dim_1: Fraction(2)})

    assert (
        DerivedUnit(
            symbol=None,
            unit_exponents={base_dim_1: Fraction(3, 2)},
        )
        * DerivedUnit(
            symbol=None, unit_exponents={base_dim_1_alt: Fraction(-3, 2)}
        )
    ).dimensions() == Dimensions({})


def test_derived_unit_si_parameters():
    x_unit = BaseUnit("x", dim_1, 7)
    y_unit = BaseUnit("y", dim_2, 5)

    derived_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            x_unit: Fraction(2),
            y_unit: Fraction(3),
        },
        factor=11,
        offset=13,
    )

    assert derived_unit.si_offset() == 13
    assert derived_unit.si_factor() == 11 * 7**2 * 5**3


def test_derived_unit_multiplicative_inverse():
    x_unit = BaseUnit("x", dim_1, 7)
    y_unit = BaseUnit("y", dim_2, 5)

    derived_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            x_unit: Fraction(2),
            y_unit: Fraction(3),
        },
        factor=11,
    )

    assert derived_unit.multiplicative_inverse() == DerivedUnit(
        symbol=None,
        unit_exponents={
            x_unit: Fraction(-2),
            y_unit: Fraction(-3),
        },
        factor=1 / 11,
    )

    with pytest.raises(ValueError):
        DerivedUnit(
            symbol=None,
            unit_exponents={
                x_unit: Fraction(2),
                y_unit: Fraction(3),
            },
            factor=0,
            offset=1,
        ).multiplicative_inverse()


def test_derived_unit_as_quantity():
    x_unit = BaseUnit("x", dim_1, 7)
    y_unit = BaseUnit("y", dim_2, 5)

    non_offset_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            x_unit: Fraction(2),
            y_unit: Fraction(3),
        },
        factor=11,
    )

    assert non_offset_unit.as_quantity() == Quantity(1, non_offset_unit)

    offset_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            x_unit: Fraction(2),
            y_unit: Fraction(3),
        },
        factor=11,
        offset=13,
    )

    assert offset_unit.as_quantity() != Quantity(0, non_offset_unit)


def test_rename_derived_unit():
    new_derived = derived_complicated.as_derived_unit("new_derived")
    new_derived_2 = DerivedUnit.using(new_derived, "new_derived")

    assert new_derived == new_derived_2


def test_derived_unit_using():
    a_derived_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=11,
        offset=13,
    )

    b_derived_unit = DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=17,
        offset=19,
    )

    assert (
        DerivedUnit.using(
            a_derived_unit,
            factor=17 / 11,
            offset=19 - 13,
        )
        == b_derived_unit
    )


def test_derived_unit_eq():
    assert DerivedUnit(None, {}) != BaseUnit("x", dim_1, 1)

    assert DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    ) != DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(11),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    )

    assert DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    ) != DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=11,
        offset=7,
    )

    assert DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    ) == DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=11,
    )

    assert DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    ) == DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(2),
            base_dim_2: Fraction(3),
        },
        factor=5,
        offset=7,
    )


def test_derived_unit_order():
    small_du = DerivedUnit(
        symbol=None,
        unit_exponents={
            base_dim_1: Fraction(1),
        },
        factor=1,
        offset=0,
    )
