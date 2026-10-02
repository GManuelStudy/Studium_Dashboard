from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Model.pruefungsleistung import Pruefungsleistung
    from Model.semester import Semester

@dataclass
class Modul:
    modulcode : str
    modulname : str
    ects : int
    semester : Semester
    pruefungsleistungen : list[Pruefungsleistung] = field(default_factory=list)
