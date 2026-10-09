from abc import ABC, abstractmethod
from Model.studiengang import Studiengang

class StudiengangRepositoryAbstract(ABC):
    """Repository Abstract mit grundlegenden CRUD-Funktionen"""
    @abstractmethod
    def speichern(self, studiengang: Studiengang) -> Studiengang:
        """Speichert ein Studiengang"""
        pass

    @abstractmethod
    def lade_studiengang(self, studiengang: Studiengang) -> Studiengang:
        """Lade Studiengang"""
        pass

    @abstractmethod
    def lade_alle(self) -> list[Studiengang]:
        """Lade alle Studiengaenge"""
        pass

    @abstractmethod
    def lade_studiengang_von_student(self, matrikelnummer: str):
        """Lade Studiengang eines Studenten"""
        pass

    @abstractmethod
    def aktualisieren(self, studiengang: Studiengang, bezeichnung_neu: str) -> None:
        """Aktualisiert ein Studiengang"""
        pass

    @abstractmethod
    def loeschen(self, studiengang: Studiengang) -> None:
        """Löscht ein Studiengang"""
        pass

    @abstractmethod
    def lade_studiengang_id(self, studiengang: Studiengang) -> int:
        """Lade Studiengang ID"""
        pass

    @abstractmethod
    def lade_von_id(self, id: int) -> Studiengang:
        """Lade Studiengang nach technischer Datenbank-ID"""
        pass