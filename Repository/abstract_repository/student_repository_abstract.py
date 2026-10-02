import datetime
from abc import ABC, abstractmethod
from Model.student import Student
from Model.studiengang import Studiengang

class StudentRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, student: Student) -> None:
        pass

    @abstractmethod
    def lade_student(self, matrikelnummer: str) -> Student:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Student]:
        pass

    @abstractmethod
    def aktualisieren(self, student: Student, vorname_neu:str, nachname_neu:str, matrikelnummer_neu:str, studiengang: Studiengang, notendurchschnitt_ziel:float, beginndatum_neu: datetime, zielabschlussdatum_neu: datetime) -> None:
        pass

    @abstractmethod
    def loeschen(self, matrikelnummer: str) -> None:
        pass
