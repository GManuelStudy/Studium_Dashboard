from abc import ABC, abstractmethod
from Model.pruefungsleistung import Pruefungsleistung
from Model.student import Student
from Model.studiengang import Studiengang


class PruefungsleistungRepositoryAbstract(ABC):
    """Repository Abstract mit grundlegenden CRUD-Funktionen"""
    @abstractmethod
    def speichern(self, pruefungsleistung: Pruefungsleistung, studiengang: Studiengang) -> None:
        """Speichert eine Prüfungsleistung"""
        pass

    @abstractmethod
    def lade_pruefungsleistung(self, pruefungsleistung: Pruefungsleistung) -> Pruefungsleistung:
        """Lade Prüfungsleistung"""
        pass

    @abstractmethod
    def lade_alle(self) -> list[Pruefungsleistung]:
        """Lade alle Prüfungsleistungen"""
        pass

    @abstractmethod
    def lade_pruefungsleistung_von_student(self, student: Student) -> list[Pruefungsleistung]:
        """Lade Prüfungsleistungen eines Studenten."""
        pass

    @abstractmethod
    def aktualisieren(self, pruefungsleistung: Pruefungsleistung) -> None:
        """Aktualisiert Prüfungsleistung"""
        pass

    @abstractmethod
    def loeschen(self, pruefungsleistung: Pruefungsleistung) -> None:
        """Löscht Prüfungsleistung"""
        pass

    @abstractmethod
    def loesche_pruefungsleistungen_von_student(self, student: Student) -> None:
        """Löscht alle Prüfungsleistungen eines Studenten"""
        pass
