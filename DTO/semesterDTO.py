from dataclasses import dataclass, field

from DTO.modulDTO import ModulDTO
from Model.semester import Semester
from Model.status import Status

@dataclass
class SemesterDTO:
    semester: Semester
    notendurchschnitt: float
    status: Status
    module: list[ModulDTO] = field(default_factory=list)