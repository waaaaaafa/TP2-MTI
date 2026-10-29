from academicelement import AcademicElement

class Module(AcademicElement):
    def __init__(self, name="", title="", coef=1, credit=1, hours_lecture=1.5,
                 hours_td=0, hours_tp=0, teaching_mode="In-person",
                 continous_percent=40, exam_percent=60):
        super().__init__(name, title)
        self.coef, self.credit = coef, credit
        self.hours_lecture, self.hours_td, self.hours_tp = hours_lecture, hours_td, hours_tp
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent
        self.total_hours = self._WEEKS * (hours_lecture + hours_td + hours_tp)
        self._grades = {"tp": 0, "td": 0, "exam": 0}

    def set_grade(self, tp=None, td=None, exam=None):
        if tp is not None: self._grades["tp"] = tp
        if td is not None: self._grades["td"] = td
        if exam is not None: self._grades["exam"] = exam

    def summary(self):
        return (f"Module: {self.title} ({self.name})\nCoef: {self.coef}, Credits: {self.credit}\n"
                f"Hours: total {self.total_hours}, {self.hours_lecture} C, {self.hours_td} TD, {self.hours_tp} TP\n"
                f"Mode: {self.teaching_mode}, Continuous: {self.evaluation_continous_percent}% "
                f"Exam: {self.evaluation_exam_percent}%")

    def calculate_average(self):
        cc = self.evaluation_continous_percent
        p_tp = p_td = 0
        if self.hours_tp and self.hours_td:
            p_tp = p_td = cc / 2
        elif self.hours_td:
            p_td = cc
        elif self.hours_tp:
            p_tp = cc
        g = self._grades
        return (g["tp"] * p_tp + g["td"] * p_td + g["exam"] * self.evaluation_exam_percent) / 100

    def calculate_credits(self):
        return self.credit if self.calculate_average() >= 10 else 0