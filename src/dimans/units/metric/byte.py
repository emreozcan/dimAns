from ..metric_utils import (
    make_metric_units as _make_metric_units,
    make_binary_metric_units as _make_binary_metric_units,
)
from ... import BaseUnit as _BaseUnit
from ...dimension import dimensions as _dimensions

_data_dimension = _dimensions.get_or_register("data", "D")

byte = _BaseUnit(symbol="B", factor=8, dimension=_data_dimension)

(
    quettabyte,
    yottabyte,
    zettabyte,
    exabyte,
    petabyte,
    terabyte,
    gigabyte,
    megabyte,
    kilobyte,
    hectobyte,
    decabyte,
    decibyte,
    centibyte,
    millibyte,
    microbyte,
    nanobyte,
    picobyte,
    femtobyte,
    attobyte,
    zeptobyte,
    yoctobyte,
    rontobyte,
    quectobyte,
) = _make_metric_units(byte)

(
    kibibyte,
    mebibyte,
    gibibyte,
    tebibyte,
    pebibyte,
    exbibyte,
    zebibyte,
    yobibyte,
) = _make_binary_metric_units(byte)
