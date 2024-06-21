from ..imperial.length import (
    inch as _inch,
)
from ...constants import speed_of_light_in_vacuum as _c
from ..si_base.second import nanosecond as _nanosecond
from ..si_base.metre import (
    millimetre as _millimetre,
    kilometre as _kilometre,
)

horizontal_pitch = (0.2 * _inch).as_derived_unit("HP")
hammer_unit = (0.25 * _inch).as_derived_unit("Hammer unit")
rack_unit = (1.75 * _inch).as_derived_unit("U")
light_nanosecond = (_c * _nanosecond).as_derived_unit("light-nanosecond")
metric_foot = (300 * _millimetre).as_derived_unit("metric ft")
earth_radius = (6_371 * _kilometre).as_derived_unit("R_⊕")
lunar_distance = (384_399 * _kilometre).as_derived_unit("LD")
