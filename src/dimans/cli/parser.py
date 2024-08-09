import inspect
import math
import operator
import sys
from collections.abc import Mapping, Callable
from fractions import Fraction
from pathlib import Path
import re
from typing import TypeVar

from lark import Lark, Transformer, v_args, Token, Tree

from .. import (
    units,
    constants,
    dimension,
    Quantity,
    Unit,
    Dimensional,
    DerivedUnit, Dimensions
)
from ..units import unusual as units_unusual, hertz


class CalcError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


non_letter_regex = re.compile(r"[^a-zA-Z]")

with open(Path(__file__).parent / "cli.lark", "r", encoding="utf-8") as f:
    calculator_grammar = f.read()
parser = Lark(
    grammar=calculator_grammar,
    start="expr",
    parser="earley",
    propagate_positions=True,
)


def create_ident_map() -> dict[str, Unit | Quantity | float]:
    # region get the list of all units and constants
    unit_list: list[tuple[str, Unit]] = [
        x
        for x in (
            *(units.__dict__.items()),
            *(units_unusual.__dict__.items()),
        )
        if isinstance(x[1], Unit)
    ]

    constant_list: list[tuple[str, Quantity | float]] = [
        x
        for x in constants.__dict__.items()
        if isinstance(x[1], (Quantity, float, int))
    ]
    # endregion

    ident_map: dict[str, Unit | Quantity | float] = {
        "c": constants.speed_of_light_in_vacuum,
        "h": constants.planck_constant,
        "hbar": constants.reduced_planck_constant,
        "mu": constants.vacuum_magnetic_permeability,
        "mu0": constants.vacuum_magnetic_permeability,
        "z": constants.characteristic_impedance_of_vacuum,
        "z0": constants.characteristic_impedance_of_vacuum,
        "epsilon": constants.vacuum_electric_permittivity,
        "epsilon0": constants.vacuum_electric_permittivity,
        "e0": constants.vacuum_electric_permittivity,
        "k": constants.boltzmann_constant,
        "G": constants.newtonian_constant_of_gravitation,
        "ke": constants.coulomb_constant,
        "lambda": constants.cosmological_constant,
        "sigma": constants.stefan_boltzmann_constant,
        "c1": constants.first_radiation_constant,
        "c1l": constants.first_radiation_constant_for_spectral_radiance,
        "c2": constants.second_radiation_constant,
        "b": constants.wien_wavelength_displacement_law_constant,
        "bprime": constants.wien_frequency_displacement_law_constant,
        "b'": constants.wien_frequency_displacement_law_constant,
        "bentropy": constants.wien_entropy_displacement_law_constant,
        "qe": constants.elementary_charge,
        "g0": constants.conductance_quantum,
        "rk": constants.von_klitzing_constant,
        "rj": constants.josephson_constant,
        "phi0": constants.magnetic_flux_quantum,
        "alpha": constants.fine_structure_constant,
        "me": constants.electron_mass,
        "mp": constants.proton_mass,
        "mn": constants.neutron_mass,
        "mtau": constants.tau_mass,
        "mt": constants.top_quark_mass,
        "wz": constants.w_to_z_mass_ratio,
        "ge": constants.electron_g_factor,
        "gmu": constants.muon_g_factor,
        "gp": constants.proton_g_factor,
        "mub": constants.bohr_magneton,
        "mun": constants.nuclear_magneton,
        "re": constants.classical_electron_radius,
        "sigmae": constants.thomson_cross_section,
        "alpha0": constants.bohr_radius,
        "eh": constants.hartree_energy,
        "ry": constants.rydberg_unit_of_energy,
        "rinf": constants.rydberg_constant,
        "rinfty": constants.rydberg_constant,
        "rinfinity": constants.rydberg_constant,
        "na": constants.avogadro_constant,
        "nakb": constants.molar_gas_constant,
        "nae": constants.faraday_constant,
        "nah": constants.molar_planck_constant,
        "m12c": constants.atomic_mass_of_carbon_12,
        "nam12c": constants.molar_mass_of_carbon_12,
        "vmsi": constants.molar_volume_of_silicon,
        "deltavcs": constants.hyperfine_transition_frequency_of_cesium_133,
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    for ident, constant in constant_list:
        constant = 1.0 * constant
        ident_map[ident] = constant
        name = non_letter_regex.sub("", ident)
        ident_map[name] = constant
        if name.endswith("_constant"):
            ident_map[name[:-9]] = constant
        elif name.endswith("constant"):
            ident_map[name[:-8]] = constant

    for ident, unit in unit_list:
        unit = unit.as_derived_unit(unit.symbol)
        unit = DerivedUnit(
            symbol=unit.symbol,
            unit_exponents=unit.unit_exponents,
            factor=unit.factor,
            offset=unit.offset,
        )
        ident_map[ident] = unit
        name = non_letter_regex.sub("", ident)
        ident_map[name] = unit
        if name != "inch" and name[-1] != "s":
            ident_map[name + "s"] = unit
        else:
            ident_map[name + "es"] = unit
        if name[-1] == "y":
            ident_map[name[:-1] + "ies"] = unit
        if name.endswith("metre"):
            ident_map[name[:-5] + "meter"] = unit
            ident_map[name[:-5] + "meters"] = unit
        elif name.endswith("litre"):
            ident_map[name[:-5] + "liter"] = unit
            ident_map[name[:-5] + "liters"] = unit
        if unit.symbol is None:
            continue
        symbol = unit.symbol.replace(" ", "")
        if name == symbol:
            continue
        ident_map[symbol] = unit

    ident_map.update(
        {
            "'": ident_map["arcminute"],
            "''": ident_map["arcsecond"],
            '"': ident_map["arcsecond"],
            "`": ident_map["arcminute"],
            "``": ident_map["arcsecond"],
            "′": ident_map["arcminute"],
            "″": ident_map["arcsecond"],
            "°": ident_map["degree"],
            "deg": ident_map["degree"],
            "oC": ident_map["celsius"],
            "oF": ident_map["fahrenheit"],
            "gon": ident_map["gradian"],
            "feet": ident_map["foot"],
            "inf": float("inf"),
            "infty": float("inf"),
            "infinity": float("inf"),
            "nan": float("nan"),
            "NaN": float("nan"),
            "c": ident_map["speedoflightinvacuum"],
        }
    )

    return ident_map


KT = TypeVar("KT")
VT = TypeVar("VT")


def reverse_map(__map: Mapping[KT, VT], /) -> dict[VT, list[KT]]:
    reversed_map = {}
    for k, v in __map.items():
        if v not in reversed_map:
            reversed_map[v] = [k]
        else:
            reversed_map[v].append(k)
    return reversed_map


def raiser(x: Exception, /):
    raise x


def create_functions_map() -> dict[str, Callable]:
    def factorial(x):
        if not isinstance(x, int):
            x = int(x)
        if x > 2 ** 8:
            raise OverflowError("argument must not be greater than 2^8")
        return math.factorial(x)

    func_map = {}

    # region add math.* functions
    func_map.update({
        # One argument functions

        "ceil": lambda x: math.ceil(x),
        "abs": lambda x: x if x >= 0 else -x,
        "factorial": factorial,
        "floor": lambda x: math.floor(x),
        "isfinite": lambda x: math.isfinite(x),
        "isinf": lambda x: math.isinf(x),
        "isnan": lambda x: math.isnan(x),
        "isqrt": lambda x: math.isqrt(x),
        "trunc": lambda x: math.trunc(x),
        "cbrt": lambda x: x ** (Fraction(1, 3)),
        "exp": lambda x: math.exp(x),
        "exp2": lambda x: dimensional_pow(2.0, x),
        "expm1": lambda x: math.expm1(x),
        "log": lambda x, base=math.e: math.log(x, base),
        "log1p": lambda x: math.log1p(x),
        "log2": lambda x: math.log2(x),
        "log10": lambda x: math.log10(x),
        "sqrt": lambda x: x ** (Fraction(1, 2)),
        "acos": lambda x: math.acos(x),
        "asin": lambda x: math.asin(x),
        "atan": lambda x: math.atan(x),
        "cos": lambda x: math.cos(x),
        "sin": lambda x: math.sin(x),
        "tan": lambda x: math.tan(x),
        "acosh": lambda x: math.acosh(x),
        "asinh": lambda x: math.asinh(x),
        "atanh": lambda x: math.atanh(x),
        "cosh": lambda x: math.cosh(x),
        "sinh": lambda x: math.sinh(x),
        "tanh": lambda x: math.tanh(x),
        "erf": lambda x: math.erf(x),
        "erfc": lambda x: math.erfc(x),
        "gamma": lambda x: math.gamma(x),
        "lgamma": lambda x: math.lgamma(x),
        "degrees": lambda x: math.degrees(x),
        "radians": lambda x: math.radians(x),

        "neg": lambda x: -x,

        # Two parameter functions
        "comb": lambda x, y: math.comb(x, y),
        "copysign": lambda x, y: abs(x) * int(math.copysign(1, y)),
        "perm": lambda x, y: math.perm(x, y),
        "pow": lambda x, y: x ** y,
        "atan2": lambda x, y: math.atan2(x, y),
        "dist": lambda x, y: math.sqrt(x ** 2 + y ** 2),
        "mod": lambda x, y: operator.mod(x, y),

        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "div": lambda x, y: x / y,
    })

    # endregion

    # region add our functions
    def func_dim(x):
        if isinstance(x, Dimensional):
            return x.dimensions()
        raise Exception("value is not Dimensional")

    func_map["dim"] = func_dim

    def func_unit(x):
        if isinstance(x, Quantity):
            return x.unit
        if isinstance(x, Unit):
            return x
        raise Exception("value does not have a unit")

    func_map["unit"] = func_unit

    def func_val(x):
        if isinstance(x, Quantity):
            return x.value
        raise Exception("value is not a Quantity")

    func_map["val"] = func_val

    def func_uval(x):
        if isinstance(x, Quantity):
            return x.underlying_value()
        raise Exception("value is not a Quantity")

    func_map["uval"] = func_uval

    def func_exit():
        sys.exit(0)

    func_map["exit"] = func_exit
    # endregion

    # region add functions that are handled by the interpreter
    func_map.update({
        "r": lambda x: raiser(NotImplementedError()),
    })
    # endregion

    # mypy says that we return "dict[str, function]" instead of the annotated
    # "dict[str, Callable]" and that they're incompatible, apparently.
    return func_map  # type: ignore


def dimensional_pow(left, right) -> float:
    if isinstance(left, Dimensional):
        right = Fraction(right).limit_denominator()
    return left ** right


CalcOutcome = Quantity | Unit | float
CalcResult = CalcOutcome | list[CalcOutcome]
ResultListType = list[tuple[str, Tree, CalcResult]]


@v_args(inline=True)
class CalculatorEvaluator(Transformer):

    ident_map = create_ident_map()
    reverse_ident_map = reverse_map(ident_map)
    func_map = create_functions_map()

    def __init__(self) -> None:
        super().__init__()
        self.results: ResultListType = []

    add = staticmethod(operator.add)
    sub = staticmethod(operator.sub)
    mul = staticmethod(operator.mul)
    div = staticmethod(operator.truediv)
    mod = staticmethod(operator.mod)
    neg = staticmethod(operator.neg)
    pos = staticmethod(operator.pos)
    str = str
    number = float

    pow = staticmethod(dimensional_pow)


    def ident(self, name: Token):
        try:
            return self.ident_map[name]
        except KeyError:
            if name in self.func_map:
                raise CalcError(f"Unknown identifier {name.value!r}\n"
                                f"However, there is a function with that name.")

            raise CalcError(f"Unknown identifier {name.value!r}")

    def convert(self, source, target):
        if not isinstance(source, Quantity):
            raise CalcError("Conversion source must be a Quantity")
        if not isinstance(target, (Quantity, Unit)):
            raise CalcError("Conversion target must be a Quantity or Unit")
        try:
            return source.to(target)
        except ValueError:
            raise CalcError(
                f"Cannot convert between incompatible units\n"
                f"    source dimensions = {source.dimensions()}\n"
                f"    target dimensions = {target.dimensions()}\n"
            )

    def sumconvert(self, *args):
        source = args[0]
        targets = list(args[1:])

        if not isinstance(source, Quantity):
            raise CalcError("Conversion source must be a Quantity")
        allowed_types = (Quantity, Unit)
        for number, target in enumerate(targets):
            if not isinstance(target, allowed_types):
                raise CalcError(
                    f"All conversion targets must be Quantity or Unit\n"
                    f"    target #{number} = {target}\n"
                )
        for i in range(len(targets)):
            if not isinstance(targets[i], Unit):
                targets[i] = targets[i].as_derived_unit()
        source_dim = source.dimensions()
        for number, target in enumerate(targets):
            target_dim = target.dimensions()
            if source_dim != target_dim:
                raise CalcError(
                    f"All conversion targets must be of compatible units\n"
                    f"    source dimensions = {source_dim}\n"
                    f"    target dimensions = {target_dim}\n"
                    f"    (target #{number}) which is {target}\n"
                )
        return source.to_terms(targets)

    def func(self, name: Token, *args):
        try:
            func_obj = self.func_map[name]
        except KeyError:
            if name in self.ident_map:
                raise CalcError(f"Unknown function {name.value!r}\n"
                                f"However, there is a value with that name.")

            raise CalcError(f"Unknown function {name.value!r}")

        sig = inspect.signature(func_obj)
        min_params = sum(
            1 for p in sig.parameters.values()
            if p.kind == p.kind.POSITIONAL_OR_KEYWORD
            and p.default is p.empty
        )
        max_params: int | None = len(sig.parameters)
        for param in sig.parameters.values():
            if param.kind == param.kind.VAR_POSITIONAL:
                max_params = None
                break

        param_count = len(args)
        if max_params is not None:
            if not (min_params <= param_count <= max_params):
                if min_params == max_params:
                    if min_params == 1:
                        raise CalcError(
                            f"Function {name.value!r} takes 1 parameter "
                            f"({param_count} given)"
                        )
                    raise CalcError(
                        f"Function {name.value!r} takes {min_params} "
                        f"parameters ({param_count} given)"
                    )
                raise CalcError(
                    f"Function {name.value!r} takes {min_params} to "
                    f"{max_params} parameters ({param_count} given)"
                )
        elif not (min_params <= param_count):
            if min_params == 1:
                raise CalcError(
                    f"Function {name.value!r} takes at least 1 parameter "
                    f"({param_count} given)"
                )
            raise CalcError(
                f"Function {name.value!r} takes at least {min_params}"
                f"parameters ({param_count} given)"
            )

        if name == "r":
            return self.function_r(*args)

        try:
            ret_val = func_obj(*args)
        except Exception as e:
            raise CalcError(f"{name.value}: {e}")

        return ret_val

    def function_r(self, index: float):
        if not isinstance(index, int):
            try:
                index = int(index)
            except (ValueError, TypeError):
                raise CalcError(f"Invalid result index '{index}'")

        try:
            return self.results[index][2]
        except IndexError:
            raise CalcError(f"Unknown result {index}")


evaluator = CalculatorEvaluator()


EMPTY_DIMENSIONS = Dimensions()
TIME_MINUS_ONE_DIMENSIONS = hertz.dimensions()


def get_canonical_unit(value: Quantity) -> Unit:
    dims = value.dimensions()
    if dims == EMPTY_DIMENSIONS:
        return value.unit

    if value.unit not in evaluator.reverse_ident_map:
        return value.unit

    if value.unit.symbol:
        return value.unit

    aliases = evaluator.reverse_ident_map[value.unit]

    if dims == TIME_MINUS_ONE_DIMENSIONS:
        aliases = [x for x in aliases if "Hz" in x]

    canonical_unit = evaluator.ident_map[min(aliases, key=len)]
    assert isinstance(canonical_unit, Unit)
    return canonical_unit


def get_longest_name(value: Quantity | float | Unit) -> str:
    if value not in evaluator.reverse_ident_map:
        return str(value)
    aliases = evaluator.reverse_ident_map[value]
    return max(aliases, key=len)


def get_shortest_name(value: Quantity | float | Unit) -> str:
    if value not in evaluator.reverse_ident_map:
        return str(value)
    aliases = evaluator.reverse_ident_map[value]
    return min(aliases, key=len)


def get_names_overview(value: Quantity | float | Unit) -> str:
    if value not in evaluator.reverse_ident_map:
        if isinstance(value, DerivedUnit):
            return value._str_with_multiplicands()
        return str(value)

    aliases = evaluator.reverse_ident_map[value]
    shortest_name = min(aliases, key=len)
    longest_name = max(aliases, key=len)

    if shortest_name == longest_name:
        return shortest_name

    return f"{longest_name} ({shortest_name})"


def get_name_of_function(func_obj, name) -> str:
    sig = inspect.signature(func_obj)
    return f"{name}{sig}"
