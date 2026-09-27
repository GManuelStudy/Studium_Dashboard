from dataclasses import dataclass, field

from datetime import datetime
from Model.student import Student
from Model.studiengang import Studiengang
from Model.semester import Semester
from Model.modul import Modul

@dataclass
class DashboardDTO:
    student: Student
    studiengang: Studiengang
    studienfortschritt: float
    aktueller_notendurchschnitt: float
    erforderliche_note: float
    studiendauer_fortschritt: float
    verbleibende_dauer: datetime
    verfuegbare_dauer_pro_modul: datetime
    semester_notendurchschnitt: float
    semester: list[Semester] = field(default_factory=list)
    module: list[Modul] = field(default_factory=list)