from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING
from Model.status import Status

# Verhindert Fehler bei Import
if TYPE_CHECKING:
    from Model.pruefungsleistung import Pruefungsleistung
    from Model.studiengang import Studiengang

@dataclass
class Student:
    """Enthält Stammdaten eines Studenten."""
    vorname: str
    nachname: str
    matrikelnummer: str
    studiengang: Studiengang
    zielnotendurchschnitt: float
    beginndatum: datetime
    zielabschlussdatum: datetime
    pruefungsleistungen: list[Pruefungsleistung] = field(default_factory=list)

    @property
    def aktuellerNotendurchschnitt(self) -> float:
        """Berechnet aktuellen Notendurchschnitt aus Prüfungsleistungen und gibt das Ergebnis zurück.
        Prüfungsleistungen mit Status.OFFEN werden nicht berücksichtigt.
        Gibt 0 zurück wenn keine Noten in Prüfungsleistungen vorhanden sind.
        """
        modul_noten = [
            item.note for item in self.pruefungsleistungen
            if item.note is not None and item.status != Status.OFFEN
        ]
        if len(modul_noten) == 0:
            return 0
        return sum(modul_noten) / len(modul_noten)

    @property
    def aktuelleECTS(self) -> int:
        """Summiert ECTS abgeschlossener Prüfungsleistungen."""
        modul_ects = [
            item.modul.ects for item in self.pruefungsleistungen
            if item.status == Status.ABGESCHLOSSEN
        ]
        return sum(modul_ects)

    @property
    def abgeschlosseneModule(self) -> int:
        """Zählt Prüfungsleistungen mit Status.ABGESCHLOSSEN und gibt das Ergebnis zurück."""
        return len([
            item for item in self.pruefungsleistungen
            if item.status == Status.ABGESCHLOSSEN
        ])

    @property
    def abgeschlosseneSemester(self) -> int:
        """Zählt Semester mit allen abgeschlossenen Modulen und gibt das Ergebnis zurück."""
        abgeschlossene_semester = 0
        for semester in self.studiengang.semester:
            module = semester.module

            if not module:
                continue

            alle_module_abgeschlossen = all(any(
                item.modul == modul and item.status == Status.ABGESCHLOSSEN
                for item in self.pruefungsleistungen
            ) for modul in module)
            if alle_module_abgeschlossen:
                abgeschlossene_semester += 1
        return abgeschlossene_semester
