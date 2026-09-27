from abc import ABC, abstractmethod
from Model.studiengang import Studiengang

class StudiengangRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, studiengang: Studiengang) -> None:
        pass

    @abstractmethod
    def lade_studiengang(self, studiengang: Studiengang) -> Studiengang:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Studiengang]:
        pass

    @abstractmethod
    def aktualisieren(self, studiengang: Studiengang, bezeichnung_neu: str) -> None:
        pass

    @abstractmethod
    def loeschen(self, studiengang: Studiengang) -> None:
        pass