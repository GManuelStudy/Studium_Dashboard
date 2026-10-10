from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

# Verhindert Fehler bei Import
if TYPE_CHECKING:
    from Model.semester import Semester

@dataclass
class Studiengang:
    """Beschreibt einen Studiengang."""
    studiengang : str
    semester : list[Semester] = field(default_factory=list)

    @property
    def ects_gesamt(self) -> float:
        """Summiert die ECTS aller Module der Semester."""
        return sum(item.ects for semester in self.semester for item in semester.module)

    @property
    def anzahl_semester(self) -> int:
        """Gibt die Anzahl der aktuell geladenen Semester zurück."""
        return len(self.semester)

    @property
    def anzahl_module(self) -> int:
        """Zählt die Module aller aktuell geladenen Semester."""
        return sum(len(semester.module) for semester in self.semester)
