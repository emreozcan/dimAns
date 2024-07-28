from ..si_base.second import second as _second

minute = (60 * _second).as_derived_unit("min")
hour = (60 * minute).as_derived_unit("h")
day = (24 * hour).as_derived_unit("d")
week = (7 * day).as_derived_unit("w")
year = (365.2425 * day).as_derived_unit("y")
month = ((1 / 12) * year).as_derived_unit("mo")
