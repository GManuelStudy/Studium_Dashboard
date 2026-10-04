from dataclasses import dataclass, field

from datetime import datetime

from dateutil.relativedelta import relativedelta

from DTO.semesterDTO import SemesterDTO
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
    notendurchschnitt_bei_erfolgreicher_note: float
    studiendauer_fortschritt: float
    verbleibende_dauer: relativedelta
    verfuegbare_dauer_pro_modul: float| None
    semester: list[SemesterDTO] = field(default_factory=list)