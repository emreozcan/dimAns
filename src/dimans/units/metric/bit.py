from ..metric_utils import (
    make_metric_units as _make_metric_units,
    make_binary_metric_units as _make_binary_metric_units,
)
from ... import BaseUnit as _BaseUnit
from ...dimension import dimensions as _dimensions

_data_dimension = _dimensions.get_or_register("data", "D")

bit = _BaseUnit(symbol="b", factor=1, dimension=_data_dimension)

(
    quettabit,
    yottabit,
    zettabit,
    exabit,
    petabit,
    terabit,
    gigabit,
    megabit,
    kilobit,
    hectobit,
    decabit,
    decibit,
    centibit,
    millibit,
    microbit,
    nanobit,
    picobit,
    femtobit,
    attobit,
    zeptobit,
    yoctobit,
    rontobit,
    quectobit,
) = _make_metric_units(bit)

(
    kibibit,
    mebibit,
    gibibit,
    tebibit,
    pebibit,
    exbibit,
    zebibit,
    yobibit,
) = _make_binary_metric_units(bit)
