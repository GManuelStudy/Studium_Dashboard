from abc import ABC, abstractmethod
from Model.semester import Semester
from Model.studiengang import Studiengang


class SemesterRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, semester: Semester) -> None:
        pass

    @abstractmethod
    def lade_semester(self, semester: Semester) -> Semester:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Semester]:
        pass

    @abstractmethod
    def lade_semester_von_studiengang(self, studiengang: Studiengang) -> list[Semester]:
        pass

    @abstractmethod
    def aktualisieren(self, semester: Semester, semester_neu: int | None = None) -> None:
        pass

    @abstractmethod
    def loeschen(self, semester: Semester) -> None:
        pass
