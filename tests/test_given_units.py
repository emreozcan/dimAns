
import dimans
import dimans.constants
import dimans.units.unusual
from dimans.base_classes import Unit


def test_units_are_unique_by_symbol():
    units: list[tuple[str, Unit]] = [
        x
        for x in (
            *(dimans.units.__dict__.items()),
            *(dimans.units.unusual.__dict__.items()),
        )
        if isinstance(x[1], Unit)
    ]
    symbol_unit_map: dict[str, list[Unit]] = {}
    for _, unit in units:
        if unit.symbol not in symbol_unit_map:
            symbol_unit_map[unit.symbol] = [unit]
            continue
        symbol_unit_map[unit.symbol].append(unit)

    for symbol, units in symbol_unit_map.items():
        assert len(units) == 1, f"Multiple units with symbol {symbol}: {units}"


def test_units_are_unique_by_ident():
    units: list[tuple[str, Unit]] = [
        x
        for x in (
            *(dimans.units.__dict__.items()),
            *(dimans.units.unusual.__dict__.items()),
        )
        if isinstance(x[1], Unit)
    ]
    ident_unit_map: dict[str, list[Unit]] = {}
    for ident, unit in units:
        if ident not in ident_unit_map:
            ident_unit_map[ident] = [unit]
            continue
        ident_unit_map[ident].append(unit)

    for ident, units in ident_unit_map.items():
        assert len(units) == 1, f"Multiple units with ident {ident}: {units}"
