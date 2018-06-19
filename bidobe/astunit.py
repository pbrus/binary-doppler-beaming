"""
Store physical constants and calculate astronomical units
from and to the International System of Units.

"""
class UnitsConverter:
    """UnitsConverter converts different astronomical units
    from and to the International System of Units (SI).
    """

    # All constants in SI units.
    G = 6.67408e-11
    LIGHT_SPEED = 2.99792458e8
    PLANCK_CONSTANT = 6.62606979e-34
    BOLTZMANN_CONSTANT = 1.38064852e-23
    STEFAN_BOLTZMANN_CONSTANT = 5.670367e-8
    SUN_MASS = 1.9884e30
    SUN_RADIUS = 6.957e8
    AU = 1.49597e11
    PARSEC = 3.086e16
    DAY = 86400
    MINUTE = 60

    def convert_sun_mass_to_kg(self, mass):
        """Convert mass in the solar mass to kilograms."""
        return mass*self.SUN_MASS

    def convert_kg_to_sun_mass(self, mass):
        """Convert mass in kilograms to the solar mass."""
        return mass/self.SUN_MASS

    def convert_days_to_sec(self, days):
        """Convert time in days to seconds."""
        return days*self.DAY

    def convert_sec_to_days(self, seconds):
        """Convert time in seconds to days."""
        return seconds/self.DAY

    def convert_min_to_sec(self, minutes):
        """Convert time in minutes to seconds."""
        return self.MINUTE*minutes

    def convert_sec_to_min(self, seconds):
        """Convert time in seconds to minutes."""
        return seconds/self.MINUTE

    def convert_hours_to_sec(self, minutes):
        """Convert time in hours to seconds."""
        return (self.MINUTE**2)*minutes

    def convert_sec_to_hours(self, seconds):
        """Convert time in seconds to hours."""
        return seconds/(self.MINUTE**2)

    def convert_au_to_m(self, au):
        """Convert length in the Astronomical Units to meters."""
        return au*self.AU

    def convert_m_to_au(self, meters):
        """Convert length in meters to the Astronomical Units."""
        return meters/self.AU

    def convert_kmps_to_mps(self, speed):
        """Convert speed in kilometers per second to meters per second."""
        return 1000.0*speed

    def convert_mps_to_kmps(self, speed):
        """Convert speed in meters per second to kilometers per second."""
        return speed/1000.0

    def convert_m_to_sun_radius(self, meters):
        """Convert length in meters to the solar radius."""
        return meters/self.SUN_RADIUS

    def convert_sun_radius_to_m(self, radii):
        """Convert length in the solar radius to meters."""
        return self.SUN_RADIUS*radii

    def convert_m_to_parsec(self, meters):
        """Convert length in meters to parsec."""
        return meters/self.PARSEC

    def convert_parsec_to_m(self, parsecs):
        """Convert length in parsec to meters."""
        return parsecs*self.PARSEC
