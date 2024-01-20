from ..si_base.gram import (
    yottagram as _yottagram,
    exagram as _exagram,
)

jupiter_mass = (1_898_130 * _yottagram).as_derived_unit("M_J")
solar_mass = (1_988_470 * _yottagram).as_derived_unit("M_☉")
earth_mass = (5_972_370 * _exagram).as_derived_unit("M_⊕")
