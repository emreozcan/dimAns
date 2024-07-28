from ..si_derived.watt import kilowatt as _kilowatt
from ..common.time import hour as _hour
from ..metric.calorie import gigacalorie as _gigacalorie
from ..metric_utils import make_metric_units as _make_metric_units
from ..common.energy import british_thermal_unit as _british_termal_unit
from ..si_derived.joule import joule as _joule

gasoline_gallon_equivalent = (33.7 * _kilowatt * _hour).as_derived_unit(
    "gasoline gallon equivalent"
)

tons_of_tnt_equivalent = _gigacalorie.as_derived_unit("ton of TNT equivalent")
(
    quettatons_of_tnt_equivalent,
    yottatons_of_tnt_equivalent,
    zettatons_of_tnt_equivalent,
    exatons_of_tnt_equivalent,
    petatons_of_tnt_equivalent,
    teratons_of_tnt_equivalent,
    gigatons_of_tnt_equivalent,
    megatons_of_tnt_equivalent,
    kilotons_of_tnt_equivalent,
    hectotons_of_tnt_equivalent,
    decatons_of_tnt_equivalent,
    decitons_of_tnt_equivalent,
    centitons_of_tnt_equivalent,
    millitons_of_tnt_equivalent,
    microtons_of_tnt_equivalent,
    nanotons_of_tnt_equivalent,
    picotons_of_tnt_equivalent,
    femtotons_of_tnt_equivalent,
    attotons_of_tnt_equivalent,
    zeptotons_of_tnt_equivalent,
    yoctotons_of_tnt_equivalent,
    rontotons_of_tnt_equivalent,
    quectotons_of_tnt_equivalent,
) = _make_metric_units(tons_of_tnt_equivalent)

halifax_explosion = (3 * kilotons_of_tnt_equivalent).as_derived_unit(
    "Halifax explosion"
)
hiroshima_bomb = (15 * kilotons_of_tnt_equivalent).as_derived_unit(
    "Hiroshima bomb"
)
quad = (10**15 * _british_termal_unit).as_derived_unit("Q")
foe = (10**44 * _joule).as_derived_unit("foe")
