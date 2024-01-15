from fractions import Fraction as _Fraction
from math import pi as _pi

from .units import metric as _metric
from .units import si as _si


speed_of_light_in_vacuum = (299_792_458 * _si.metre) / _si.second
planck_constant = (_Fraction(662607015, 10 ** 42) * _si.joule) / _si.hertz
reduced_planck_constant = planck_constant / (2 * _pi)
vacuum_magnetic_permeability = _Fraction(
    12566370621219,
    10000000000000 * 10**6
) * _si.newton / _si.ampere ** 2
characteristic_impedance_of_vacuum = vacuum_magnetic_permeability \
                                     * speed_of_light_in_vacuum
vacuum_electric_permittivity = (
    vacuum_magnetic_permeability * speed_of_light_in_vacuum ** 2
).multiplicative_inverse()
boltzmann_constant = _Fraction(
    1380649,
    1000000 * 10 ** 23
) * _si.joule / _si.kelvin
newtonian_constant_of_gravitation = _Fraction(
    66743015,
    10000000 * 10 ** 11
) * _si.metre ** 3 * _si.kilogram ** -1 * _si.second ** -2
coulomb_constant = (
    4 * _pi * vacuum_electric_permittivity
).multiplicative_inverse()
cosmological_constant = _Fraction(
    108929,
    100000 * 10**52
) * _si.metre ** -2
stefan_boltzmann_constant = (
    (_pi ** 2 * boltzmann_constant ** 4)
    / (60 * reduced_planck_constant ** 3 * speed_of_light_in_vacuum ** 2)
)
first_radiation_constant = (
    2
    * _pi
    * planck_constant
    * speed_of_light_in_vacuum ** 2
)
first_radiation_constant_for_spectral_radiance = (
    2 * planck_constant * speed_of_light_in_vacuum ** 2
) / _si.steradian
second_radiation_constant = (
    planck_constant * speed_of_light_in_vacuum / boltzmann_constant
)
wien_wavelength_displacement_law_constant = _Fraction(
    2897771955,
    1000000000 * 10**3
) * _si.metre * _si.kelvin
wien_frequency_displacement_law_constant = _Fraction(
    5878925757,
    1000000000
) * 10 ** 10 * _si.hertz * _si.kelvin ** -1
wien_entropy_displacement_law_constant = _Fraction(
    3002916077,
    1000000000 * 10**3
) * _si.metre * _si.kelvin
elementary_charge = _Fraction(
    1602176634,
    1000000000 * 10**19
) * _si.coulomb
conductance_quantum = 2 * elementary_charge ** 2 / planck_constant
inverse_conductance_quantum = planck_constant / (2 * elementary_charge ** 2)
von_klitzing_constant = planck_constant / elementary_charge ** 2
josephson_constant = 2 * elementary_charge / planck_constant
magnetic_flux_quantum = planck_constant / (2 * elementary_charge)
fine_structure_constant = elementary_charge ** 2 / (
    4 * _pi * vacuum_electric_permittivity * reduced_planck_constant
    * speed_of_light_in_vacuum
)
inverse_fine_structure_constant = fine_structure_constant ** -1
electron_mass = _Fraction(
    9109383701528,
    1000000000000 * 10**31
) * _si.kilogram
proton_mass = _Fraction(
    16726219236951,
    10000000000000 * 10**27
) * _si.kilogram
neutron_mass = _Fraction(
    16749274980495,
    10000000000000 * 10**27
) * _si.kilogram
muon_mass = _Fraction(
    188353162742,
    100000000000 * 10**28
) * _si.kilogram
tau_mass = _Fraction(
    31675421,
    10000000 * 10**27
) * _si.kilogram
top_quark_mass = _Fraction(
    3078453,
    1000000 * 10**25
) * _si.kilogram
proton_to_electron_mass_ratio = proton_mass / electron_mass
w_to_z_mass_ratio = _Fraction(
     8815317,
    10000000
)
weak_mixing_angle = _Fraction(
     2229030,
    10000000
)
electron_g_factor = _Fraction(
    -20023193043625635,
     10000000000000000
)
muon_g_factor = _Fraction(
    -2002331841813,
     1000000000000
)
proton_g_factor = _Fraction(
    5585694689316,
    1000000000000
)
quantum_of_circulation = planck_constant / (2 * electron_mass)
bohr_magneton = (elementary_charge * reduced_planck_constant) / (
    2 * electron_mass
)
nuclear_magneton = (elementary_charge * reduced_planck_constant) / (
    2 * proton_mass
)
classical_electron_radius = (elementary_charge ** 2 * coulomb_constant) / (
    electron_mass * speed_of_light_in_vacuum ** 2
)
thomson_cross_section = (8 * _pi / 3) * classical_electron_radius ** 2
bohr_radius = classical_electron_radius / fine_structure_constant ** 2
hartree_energy = (
    fine_structure_constant ** 2
    * speed_of_light_in_vacuum ** 2
    * electron_mass
)
rydberg_unit_of_energy = hartree_energy / 2
rydberg_constant = (
    fine_structure_constant ** 2
    * electron_mass
    * speed_of_light_in_vacuum
) / (2 * planck_constant)
fermi_coupling_constant = _Fraction(
    1_166_37876,
    1_000_00000 * 10 ** 5
) * (_metric.gigaelectron_volt ** -2)
avogadro_constant = _Fraction(
    602214076 * 10**23,
    100000000
) / _si.mole
molar_gas_constant = avogadro_constant * boltzmann_constant
faraday_constant = avogadro_constant * elementary_charge
molar_planck_constant = avogadro_constant * planck_constant
atomic_mass_of_carbon_12 = _Fraction(
    1_922_646_879_9260,
    1_000_000_000_0000 * 10 ** 26
) * _si.kilogram
molar_mass_of_carbon_12 = atomic_mass_of_carbon_12 * avogadro_constant
atomic_mass_constant = atomic_mass_of_carbon_12 / 12
molar_mass_constant = molar_mass_of_carbon_12 / 12
molar_volume_of_silicon = _Fraction(
    1_205_883_199_60,
    1_000_000_000_00 * 10 ** 5
) * (_si.metre ** 3 / _si.mole)
hyperfine_transition_frequency_of_cesium_133 = 9_192_631_770 * _si.hertz
