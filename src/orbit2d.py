from math import sqrt, pi, pow, radians, sin, cos, atan2, asin
from scipy.optimize import fsolve
from astro_units import *


class Orbit2DParameters:
    """Orbit2DParameters is a builder class for the Orbit2D objects."""

    def __init__(self, first_mass, second_mass,
                 semi_major_axis, eccentricity, periastron_passage=0.0):
        """Set basic parameters of binary system in 2D space.

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
            A moment when a star passes periastron. Default = 0.
        """
        self.first_mass = first_mass
        self.second_mass = second_mass
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.periastron_passage = periastron_passage


class Orbit2D(UnitsConverter):
    """Orbit2D represents the position and velocity vectors of any object
    in binary system. For any given time t the: x(t), y(t), v_x(t), v_y(t)
    are computed."""

    def __init__(self, orbit2d):
        self.first_mass = orbit2d.first_mass
        self.second_mass = orbit2d.second_mass
        self.semi_major_axis = orbit2d.semi_major_axis
        self.eccentricity = orbit2d.eccentricity
        self.periastron_passage = orbit2d.periastron_passage
        self.calculate_period()

    def calculate_period(self):
        """Calculate a period in seconds."""
        sum_mass = self.first_mass + self.second_mass
        self.period = sqrt(
            4*pow(pi,2)*pow(self.semi_major_axis, 3)
            /(self.G*(self.convert_sun_mass_to_kg(sum_mass))))

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

    def calculate_velocity(self):
        """Calculate velocity tuple in meters per second."""
        speed = self.calculate_speed()
        angle = self.calculate_velocity_angle()
        self.velocity = speed*cos(angle), speed*sin(angle)

        return self.velocity

    def calculate_speed(self):
        sum_mass = self.first_mass + self.second_mass
        speed_pow2 = 2/self.distance - 1/self.semi_major_axis
        speed_pow2 *= self.G*self.convert_sun_mass_to_kg(sum_mass)

        return sqrt(speed_pow2)

    def calculate_velocity_angle(self):
        sin_angle = (pow(self.semi_major_axis, 2)
                     - pow(self.eccentricity*self.semi_major_axis,2))
        sin_angle /= (self.distance*(2*self.semi_major_axis - self.distance))
        sin_angle = sqrt(sin_angle)

        if divmod(self.true_anomaly, 2*pi)[1] <= pi:
            velocity_angle = asin(sin_angle) + self.true_anomaly
        else:
            velocity_angle = pi - asin(sin_angle) + self.true_anomaly

        return velocity_angle

    def update(self, time):
        """Update x, y, v_x, v_y for particular time"""
        self.calculate_mean_anomaly(time)
        self.calculate_eccentric_anomaly()
        self.calculate_true_anomaly()
        self.calculate_distance()
        self.calculate_position()
        self.calculate_velocity()
