class UnitsConverter:
    """UnitsConverter converts different astronomical units
    from and to International System of Units (SI).
    """

    # All constant in SI units.
    G = 6.67408e-11
    SUN_MASS = 1.9884e30
    DAY = 86400
    AU = 1.49597e11

    def convert_sun_mass_to_kg(self, mass):
        return mass*self.SUN_MASS

    def convert_kg_to_sun_mass(self, mass):
        return mass/self.SUN_MASS

    def convert_days_to_sec(self, days):
        return days*self.DAY

    def convert_sec_to_days(self, seconds):
        return seconds/self.DAY

    def convert_au_to_m(self, au):
        return au*self.AU

    def convert_m_to_au(self, meters):
        return meters/self.AU
