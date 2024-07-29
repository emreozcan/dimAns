import math
import operator
from fractions import Fraction
from numbers import Number
from pathlib import Path

import regex
from lark import Lark, Transformer, v_args, Token

from .. import (
    units,
    constants,
    dimension,
    Quantity,
    BaseUnit,
    Unit,
    Dimensional,
    DerivedUnit
)
from ..units import unusual as units_unusual


class CalcError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


non_letter_regex = regex.compile(r"[^a-zA-Z]")


with open(Path(__file__).parent / "cli.lark", "r", encoding="utf-8") as f:
    calculator_grammar = f.read()
parser = Lark(
    grammar=calculator_grammar,
    start="expr",
    parser="earley",
    propagate_positions=True,
)


@v_args(inline=True)
class CalculatorEvaluator(Transformer):
    def __init__(self):
        super().__init__()

        # region get the list of all units and constants
        unit_list = [
            x
            for x in (
                *(units.__dict__.items()),
                *(units_unusual.__dict__.items()),
            )
            if isinstance(x[1], Unit)
        ]

        constant_list = [
            x
            for x in constants.__dict__.items()
            if isinstance(x[1], (Quantity, Number))
        ]
        # endregion

        ident_map = {
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
            constant: Quantity | Fraction
            constant: Quantity | float = 1.0 * constant
            name = non_letter_regex.sub("", ident)
            ident_map[name] = constant
            if name.endswith("constant"):
                ident_map[name[:-8]] = constant

        for ident, unit in unit_list:
            unit: BaseUnit | DerivedUnit
            unit = unit.as_derived_unit(unit.symbol)
            unit = DerivedUnit(
                symbol=unit.symbol,
                unit_exponents=unit.unit_exponents,
                factor=unit.factor,
                offset=unit.offset,
            )
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
        self.ident_map = ident_map

        reverse_ident_map = {}
        for k, v in self.ident_map.items():
            if v not in reverse_ident_map:
                reverse_ident_map[v] = [k]
            else:
                reverse_ident_map[v].append(k)
        self.reverse_ident_map = reverse_ident_map

        def factorial(x):
            if not isinstance(x, int):
                x = int(x)
            if x > 2**8:
                raise OverflowError("argument must not be greater than 2^8")
            return math.factorial(x)

        self.func_map = {}

        # region add math.* functions
        self.func_map.update({
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
            "exp2": lambda x: math.exp2(x),
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
            "pow": lambda x, y: x**y,
            "atan2": lambda x, y: math.atan2(x, y),
            "dist": lambda x, y: math.sqrt(x**2 + y**2),
            "mod": lambda x, y: operator.mod(x, y),

            "add": lambda x, y: x + y,
            "sub": lambda x, y: x - y,
            "mul": lambda x, y: x * y,
            "div": lambda x, y: x / y,
        })
        # endregion

        # region add our functions
        def func1_dim(x):
            if isinstance(x, Dimensional):
                return x.dimensions()
            raise Exception("value is not Dimensional")
        self.func_map["dim"] = func1_dim

        def func1_unit(x):
            if isinstance(x, Quantity):
                return x.unit
            if isinstance(x, Unit):
                return x
            raise Exception("value does not have a unit")
        self.func_map["unit"] = func1_unit

        def func1_val(x):
            if isinstance(x, Quantity):
                return x.value
            raise Exception("value is not a Quantity")
        self.func_map["val"] = func1_val

        def func1_uval(x):
            if isinstance(x, Quantity):
                return x.underlying_value()
            raise Exception("value is not a Quantity")
        self.func_map["uval"] = func1_uval
        # endregion

    add = staticmethod(operator.add)
    sub = staticmethod(operator.sub)
    mul = staticmethod(operator.mul)
    div = staticmethod(operator.truediv)
    mod = staticmethod(operator.mod)
    neg = staticmethod(operator.neg)
    str = str
    number = float

    @staticmethod
    def pow(left, right):
        if isinstance(left, Dimensional):
            right = Fraction(right).limit_denominator()
        return left ** right

    def ident(self, name: Token):
        try:
            return self.ident_map[name]
        except KeyError:
            raise CalcError(f"Unknown identifier {name.value!r}, see `?units` and `?constants`")

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
            return self.func_map[name](*args)
        except KeyError:
            raise CalcError(f"Unknown function {name.value!r}, see `?functions`")
        except Exception as e:
            raise CalcError(f"{name}: {e}")


evaluator = CalculatorEvaluator()


def get_canonical_unit(value: Quantity) -> Unit:
    if value.unit not in evaluator.reverse_ident_map:
        return value.unit

    if value.unit.symbol:
        return value.unit

    aliases = evaluator.reverse_ident_map[value.unit]

    if value.dimensions() == {dimension.dimensions.get("time"): -1}:
        aliases = [x for x in aliases if "Hz" in x]

    return evaluator.ident_map[min(aliases, key=len)]
