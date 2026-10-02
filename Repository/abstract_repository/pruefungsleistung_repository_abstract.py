from abc import ABC, abstractmethod
from Model.pruefungsleistung import Pruefungsleistung
from Model.student import Student


class PruefungsleistungRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, pruefungsleistung: Pruefungsleistung) -> None:
        pass

    @abstractmethod
    def lade_pruefungsleistung(self, pruefungsleistung: Pruefungsleistung) -> Pruefungsleistung:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Pruefungsleistung]:
        pass

    @abstractmethod
    def lade_pruefungsleistung_von_student(self, student: Student) -> list[Pruefungsleistung]:
        pass

    @abstractmethod
    def aktualisieren(self, pruefungsleistung: Pruefungsleistung) -> None:
        pass

    @abstractmethod
    def loeschen(self, pruefungsleistung: Pruefungsleistung) -> None:
        pass

    @abstractmethod
    def loesche_pruefungsleistungen_von_student(self, student: Student) -> None:
        pass
