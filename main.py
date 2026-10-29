import csv
from module import Module
from unit import Unit
from semester import Semester

def load_canvas(path):
    sems, units = {}, {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            tp, td, ex = float(r["percent_tp"]), float(r["percent_td"]), float(r["percent_exam"])
            m = Module(r["module_name"], r["module_title"], int(r["coef"]), int(r["credit"]),
                       hours_td=1.5 if td else 0, hours_tp=1.5 if tp else 0,
                       continous_percent=tp + td, exam_percent=ex)
            key = r["unite"]
            if key not in units:
                units[key] = Unit(key, r["unite_title"])
                sems.setdefault(r["semestre"], Semester(r["semestre"], "Semester " + r["semestre"])).add_unit(units[key])
            units[key].add_module(m)
    return sems

if __name__ == "__main__":
    sems = load_canvas("modules.csv")
    mod = {m.name: m for s in sems.values() for u in s.units for m in u.modules}
    mod["MTI"].set_grade(tp=14, exam=12)
    mod["RCB"].set_grade(tp=10, td=12, exam=9)
    for s in sems.values():
        print(s.name, "avg=%.2f" % s.calculate_average(), "credits=", s.calculate_credits())
        for u in s.units:
            print("  ", u.name, "avg=%.2f" % u.calculate_average(), "credits=", u.calculate_credits())