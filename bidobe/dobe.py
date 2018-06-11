from math import pow, log10, e
from bidobe.astunit import *


class OrbitingObject(UnitsConverter):
    """OrbitingObject represents a single object in binary system and its basic
    astrophysical parameters. Due to orbital motion an object's flux (doppler
    beaming) varies with time.
    """

    def __init__(self, distance, radius, temperature, passband):
        """Set basic parameters of an object in a binary system.

        Parameters
        ----------
        distance : float
            Distance to the binary system in parsecs.
        radius : float
            Radius of the object in the Sun radius.
        temperature : float
            Temperature of the object in Kelvin.
        passband : str
            The passband which the object was observed in.
            Avaible those in the convert_passband_to_frequency method.
        """
        self.distance = self.convert_parsec_to_m(distance)
        self.radius = self.convert_sun_radius_to_m(radius)
        self.temperature = temperature
        self.frequency = self.convert_passband_to_frequency(passband)
        self.calculate_stationary_flux()
        self.calculate_alpha_parameter()

    def convert_passband_to_frequency(self, passband):
        """
        Change the name of a passband to the central frequency.
        Available: U, B, V, I.
        """
        passbands_central_wavelength = {
            "U" : 3.6e-7,
            "B" : 4.4e-7,
            "V" : 5.5e-7,
            "I" : 9.0e-7
        }

        return self.LIGHT_SPEED/passbands_central_wavelength[passband]

    def calculate_stationary_flux(self):
        # For smaller temperatures than 5000K there is no sense
        # to calculate the alpha parameter and doppler beaming.
        if self.temperature > 5000:
            self.flux = pow(self.radius/self.distance,2)*pow(self.temperature,4)
            self.flux *= self.STEFAN_BOLTZMANN_CONSTANT
        else:
            self.flux = 0

        return self.flux

    def calculate_alpha_parameter(self):
        x = (self.PLANCK_CONSTANT*self.frequency
            /(self.BOLTZMANN_CONSTANT*self.temperature))
        exp_x = pow(e,x)
        self.alpha = 3 - x*exp_x/(exp_x - 1)

        return self.alpha

    def calculate_doppler_coefficient(self, radial_velocity):
        self.doppler_coefficient = 1.0 + ((3.0 - self.alpha)
                                   *radial_velocity/self.LIGHT_SPEED)

        return self.doppler_coefficient


def binary_brightness(object1, object2, zero_level=16.0):
    """
    Calculate brightness of a binary system taking into account doppler
    beaming.
    """
    doppler_flux = (object1.doppler_coefficient*object1.flux
                    + object2.doppler_coefficient*object2.flux)

    dmag = 2.5*log10(abs(doppler_flux)/(object1.flux + object2.flux))

    return zero_level + dmag
