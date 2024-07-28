from ... import DerivedUnit as _DerivedUnit
from .length import (
    rod as _rod,
    furlong as _furlong,
    chain as _chain,
    mile as _mile,
)

perch = _DerivedUnit.using(_rod**2, "perch")
rood = _DerivedUnit.using(_furlong * _rod, "rood")
acre = _DerivedUnit.using(_chain * _furlong, "acre")
square_mile = _DerivedUnit.using(_mile**2, "sq_mi")
