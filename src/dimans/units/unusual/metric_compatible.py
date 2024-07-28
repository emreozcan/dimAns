from ..si_derived.sievert import (
    nanosievert as _nanosievert,
    millisievert as _millisievert,
)
from ..common.time import hour as _hour
from ..common.energy import british_thermal_unit as _british_termal_unit
from ..si_derived import watt as _watt, hertz as _hertz
from ..si_derived.lumen import lumen as _lumen
from ..si_base.metre import metre as _metre, centimetre as _centimetre
from ..si_base.second import second as _second
from ..metric.calorie import calorie as _calorie
from ..common.angle import degree as _degree
from ..si_base.gram import hectogram as _hectogram

ton_of_refrigeration = (12_000 * _british_termal_unit / _hour).as_derived_unit(
    "TR"
)
watt_incandescent_replacement = (15 * _lumen).as_derived_unit("w")
amazon_river = (216_000 * _metre**3 / _second).as_derived_unit("Amazon River")
sverdrup = (1_000_000 * _metre**3 / _second).as_derived_unit("Sv")
langley = (_calorie / _centimetre**2).as_derived_unit("Ly")
stokes = (_centimetre**2 / _second).as_derived_unit("St")
milli_earth_rate_unit = (0.15 * _degree / _hour).as_derived_unit("MERU")
jansky = (10**-26 * _watt / _metre**2 / _hertz).as_derived_unit("Jy")
metre_of_water_equivalent = (
    100 * _hectogram / _centimetre**2
).as_derived_unit("m.w.e.")
banana_equivalent_dose = (78 * _nanosievert).as_derived_unit(
    "banana equivalent dose"
)
flight_time_equivalent_dose = ((0.004 * _millisievert / _hour)).as_derived_unit(
    "flight-time equivalent dose"
)
