from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

# Verhindert Fehler bei Import
if TYPE_CHECKING:
    from Model.pruefungsleistung import Pruefungsleistung
    from Model.semester import Semester

@dataclass
class Modul:
    """Beschreibt ein Modul. Die Zuordnung zum Studiengang erfolgt über das Semester.
    Pruefungsleistungen bleiben zunächst leer und werden erst befüllt wenn ein Student
    vorhanden ist.
    """
    modulcode: str
    modulname: str
    ects: int
    semester: Semester
    pruefungsleistungen: list[Pruefungsleistung] = field(default_factory=list)