from abc import ABC, abstractmethod
from Model.semester import Semester
from Model.studiengang import Studiengang

class SemesterRepositoryAbstract(ABC):
    """Repository Abstract mit grundlegenden CRUD-Funktionen"""
    @abstractmethod
    def speichern(self, semester: Semester) -> None:
        """Speichert ein Semester"""
        pass

    @abstractmethod
    def lade_semester(self, semester: Semester) -> Semester:
        """Lade Semester"""
        pass

    @abstractmethod
    def lade_alle(self) -> list[Semester]:
        """Lade alle Semester"""
        pass

    @abstractmethod
    def lade_semester_von_studiengang(self, studiengang: Studiengang) -> list[Semester]:
        """Lade alle Semester eines Studiengangs"""
        pass

    @abstractmethod
    def loeschen(self, semester: Semester) -> None:
        """Löscht ein Semester"""
        pass
