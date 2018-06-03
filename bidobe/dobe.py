from math import pow, log10, e


# Physical constants in SI units.

LIGHT_SPEED = 2.99792458e8
PLANCK_CONSTANT = 6.62606979e-34
BOLTZMANN_CONSTANT = 1.38064852e-23

def convert_passbands_to_frequency(passband):
    passbands_dict = {
        "U" : 3.6e-7,
        "B" : 4.4e-7,
        "V" : 5.5e-7,
        "I" : 9.0e-7
    }

    return LIGHT_SPEED/passbands_dict[passband]

def alpha_parameter(temperature, frequency):
    x = PLANCK_CONSTANT*frequency/(BOLTZMANN_CONSTANT*temperature)
    exp_x = pow(e,x)
    alpha = 3 - x*exp_x/(exp_x - 1)

    return alpha

def flux(radial_velocity, alpha):
    flux = 1 + (3 - alpha)*radial_velocity/LIGHT_SPEED

    return flux

def delta_magnitude(velocities, temperatures, passband, brightness=16.0):
    frequency = convert_passbands_to_frequency(passband)
    alpha1 = alpha_parameter(temperatures[0], frequency)
    alpha2 = alpha_parameter(temperatures[1], frequency)
    flux1 = flux(velocities[0], alpha1)
    flux2 = flux(velocities[1], alpha2)
    delta_magnitude = -2.5*log10(flux1 + flux2) + brightness

    return delta_magnitude
