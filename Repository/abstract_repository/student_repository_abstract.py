import datetime
from abc import ABC, abstractmethod
from Model.student import Student
from Model.studiengang import Studiengang

class StudentRepositoryAbstract(ABC):
    """Repository Abstract mit grundlegenden CRUD-Funktionen"""
    @abstractmethod
    def speichern(self, student: Student) -> None:
        """Speichert ein Student"""
        pass

    @abstractmethod
    def lade_student(self, matrikelnummer: str) -> Student:
        """Lade Student nach Matrikelnummer"""
        pass

    @abstractmethod
    def lade_alle(self) -> list[Student]:
        """Lade alle Studenten"""
        pass

    @abstractmethod
    def lade_alle_von_studiengang(self, studiengang: Studiengang) -> list[Student]:
        """Lade alle Studenten eines Studiengangs"""
        pass

    @abstractmethod
    def aktualisieren(
            self,
            student: Student,
            vorname_neu:str,
            nachname_neu:str,
            matrikelnummer_neu:str,
            studiengang: Studiengang,
            notendurchschnitt_ziel:float,
            beginndatum_neu: datetime,
            zielabschlussdatum_neu: datetime
    ) -> None:
        """Aktualisiert ein Student"""
        pass

    @abstractmethod
    def loeschen(self, matrikelnummer: str) -> None:
        """Löscht ein Student"""
        pass
