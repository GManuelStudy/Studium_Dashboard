from dataclasses import dataclass, field
from DTO.pruefungsleistungDTO import PruefungsleistungDTO
from Model.semester import Semester
from Model.status import Status

@dataclass
class SemesterDTO:
    """Überträgt Semesterdaten für Dashboard-DTO"""
    semester: Semester
    notendurchschnitt: float
    status: Status
    pruefungsleistung: list[PruefungsleistungDTO] = field(default_factory=list)