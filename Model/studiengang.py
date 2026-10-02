from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Model.semester import Semester

@dataclass
class Studiengang:
    studiengang : str
    semester : list[Semester] = field(default_factory=list)

    @property
    def ectsGesamt(self) -> float:
        return sum(item.ects for semester in self.semester for item in semester.module)

    @property
    def anzahlSemester(self) -> int:
        return len(self.semester)

    @property
    def anzahlModule(self) -> int:
        return sum(len(semester.module) for semester in self.semester)
