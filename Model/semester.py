from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
 # Verhindert Fehler bei Import
if TYPE_CHECKING:
    from Model.studiengang import Studiengang
    from Model.modul import Modul

@dataclass
class Semester:
    """Bildet ein Semester inkl. derer Module eines Studiengangs.
    Die Modulliste wird im Controller befüllt.
    """
    semester : int
    studiengang : Studiengang
    module : list[Modul] = field(default_factory=list)
