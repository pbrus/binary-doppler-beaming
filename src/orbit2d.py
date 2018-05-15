from math import sqrt, pi, pow, radians, sin, cos, atan2
from scipy.optimize import fsolve
from astro_units import *


class Orbit2D(UnitsConverter):
    """Orbit2D represents the position and velocity vectors of any object
    in binary system. For any given time t the: x(t), y(t), v_x(t), v_y(t)
    are computed."""

    def __init__(self, first_mass, second_mass,
                 semi_major_axis, eccentricity, periastron_passage=0.0):
        """Set basic parameters of binary system.

        Parameters
        ----------
        first_mass, second_mass : float
            Star masses of binary system. Expressed in Sun mass unit.
        semi_major_axis : float
            Semi major axis of an orbit of star which must be calculated.
            Expressed in meters.
        eccentricity : float
            A value of orbit's eccentricity between 0 and 1.
        periastron_passage : float
            A moment when a star passes periastron. Default = 0.0.
        """
        self.first_mass = first_mass
        self.second_mass = second_mass
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.periastron_passage = periastron_passage

    def calculate_period(self):
        """Calculate a period in seconds."""
        sum_mass = self.first_mass + self.second_mass
        self.period = sqrt(
            4*pow(pi,2)*pow(self.semi_major_axis, 3)
            /(G_unit*(self.convert_sun_mass_to_kg(sum_mass))))

        return self.period

    def calculate_mean_anomaly(self, time):
        """Calculate a mean anomaly in radians."""
        self.mean_anomaly = 2*pi*(time - self.periastron_passage)/self.period

        return self.mean_anomaly

    def calculate_eccentric_anomaly(self):
        """Calculate an eccentric anomaly in radians."""
        self.solve_kepler_equation()

        return self.eccentric_anomaly

    def solve_kepler_equation(self):
        self.eccentric_anomaly = fsolve(lambda x:
            self.mean_anomaly + self.eccentricity*sin(x) - x, 0.0)[0]

        return self.eccentric_anomaly

    def calculate_true_anomaly(self):
        """Calculate a true anomaly in radians."""
        x = sqrt(1 - self.eccentricity)*cos(0.5*self.eccentric_anomaly)
        y = sqrt(1 + self.eccentricity)*sin(0.5*self.eccentric_anomaly)
        self.true_anomaly = 2*atan2(y, x)

        if self.true_anomaly < 0:
            self.true_anomaly += 2*pi

        return self.true_anomaly

    def calculate_distance(self):
        """Calculate distance in meters."""
        semilatus_rectum = self.semi_major_axis*(1 - pow(self.eccentricity,2))
        self.distance = semilatus_rectum/(1
            + self.eccentricity*cos(self.true_anomaly))

        return self.distance

    def calculate_position(self):
        """Calculate position tuple in meters."""
        x_coorindate = self.distance*cos(self.true_anomaly)
        y_coorindate = self.distance*sin(self.true_anomaly)
        self.position = x_coorindate, y_coorindate

        return self.position
