from academicelement import AcademicElement

class Unit(AcademicElement):
    def __init__(self, name, title, modules=None):
        super().__init__(name, title)
        self._modules = list(modules) if modules else []
        self._refresh()

    def _refresh(self):
        self.coef = sum(m.coef for m in self._modules)
        self.credit = sum(m.credit for m in self._modules)

    def add_module(self, module):
        self._modules.append(module)
        self._refresh()

    @property
    def modules(self):
        return tuple(self._modules)

    def calculate_average(self):
        if not self._modules: return 0
        return sum(m.calculate_average() * m.coef for m in self._modules) / self.coef

    def calculate_credits(self):
        if not self._modules: return 0
        if self.calculate_average() >= 10:
            return self.credit
        return sum(m.calculate_credits() for m in self._modules)