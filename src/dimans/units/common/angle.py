from math import pi as _pi

from ..si_derived.radian import radian as _radian

degree = ((1 / 360) * _pi * _radian).as_derived_unit("°")
arcminute = ((1 / 60) * degree).as_derived_unit("′")
arcsecond = ((1 / 60) * arcminute).as_derived_unit("″")
turn = (2 * _pi * _radian).as_derived_unit("turn")
