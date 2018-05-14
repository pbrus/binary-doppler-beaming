sun_mass_kg_unit = 1.9884e30
G_unit = 6.67408e-11


class UnitsConverter:

    def __init__(self):
        pass

    def convert_sun_mass_to_kg(self, mass):
        return mass*sun_mass_kg_unit

    def convert_kg_to_sun_mass(self, mass):
        return mass/sun_mass_kg_unit
