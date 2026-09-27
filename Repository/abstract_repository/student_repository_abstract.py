from abc import ABC, abstractmethod
from Model.student import Student

class StudentRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, student: Student) -> None:
        pass

    @abstractmethod
    def lade_student(self, student: Student) -> Student:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Student]:
        pass

    @abstractmethod
    def aktualisieren(self, student: Student) -> None:
        pass

    @abstractmethod
    def loeschen(self, student: Student) -> None:
        pass
