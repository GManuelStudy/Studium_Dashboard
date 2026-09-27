from abc import ABC, abstractmethod
from Model.modul import Modul
from Model.semester import Semester

class ModulRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, modul: Modul) -> None:
        pass

    @abstractmethod
    def lade_modul(self, modul: Modul) -> Modul:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Modul]:
        pass

    @abstractmethod
    def aktualisieren(
        self, modul: Modul, modulname_neu: str | None = None,
        modulcode_neu: str | None = None, ects_neu: int | None = None,
        semester_neu: Semester | int | None = None,
    ) -> None:
        pass

    @abstractmethod
    def loeschen(self, modul: Modul) -> None:
        pass
