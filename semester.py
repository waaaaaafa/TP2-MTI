from academicelement import AcademicElement

class Semester(AcademicElement):
    def __init__(self, name, title, units=None):
        super().__init__(name, title)
        self._units = list(units) if units else []
        self._refresh()

    def _refresh(self):
        self.coef = sum(u.coef for u in self._units)
        self.credit = sum(u.credit for u in self._units)

    def add_unit(self, unit):
        self._units.append(unit)
        self._refresh()

    @property
    def units(self):
        return tuple(self._units)

    def calculate_average(self):
        if not self._units: return 0
        return sum(u.calculate_average() * u.coef for u in self._units) / self.coef

    def calculate_credits(self):
        if not self._units: return 0
        if self.calculate_average() >= 10:
            return self.credit
        return sum(u.calculate_credits() for u in self._units)