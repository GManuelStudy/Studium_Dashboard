from dataclasses import dataclass, field
from dateutil.relativedelta import relativedelta
from DTO.semesterDTO import SemesterDTO
from Model.student import Student
from Model.studiengang import Studiengang

@dataclass
class DashboardDTO:
    """Überträgt Studenten, Studiengang und weitere Kennzahlen an die Dashboard-Ansicht."""
    student: Student
    studiengang: Studiengang
    studienfortschritt: float
    aktueller_notendurchschnitt: float
    erforderliche_note: float
    notendurchschnitt_bei_erfolgreicher_note: float
    studiendauer_fortschritt: float
    verbleibende_dauer: relativedelta
    verfuegbare_dauer_pro_modul: float | None
    semester: list[SemesterDTO] = field(default_factory=list)