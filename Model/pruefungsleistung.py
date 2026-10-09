from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from Model.status import Status

# Verhindert Fehler bei Import
if TYPE_CHECKING:
    from Model.modul import Modul
    from Model.student import Student

@dataclass
class Pruefungsleistung:
    """Verknüpft Studenten mit einem Modul für ein Prüfungsergebnis.
    Noten mit dem Wert 0 oder None sind Status.OFFEN.
    Noten von 1 bis 4 sind Status.ABGESCHLOSSEN. Werte über 4 bis 5 sind Status.NICHT_BESTANDEN.
    """
    student : Student
    modul : Modul
    note : float| None
    status : Status = Status.OFFEN