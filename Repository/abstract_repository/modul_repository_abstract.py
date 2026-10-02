from abc import ABC, abstractmethod
from Model.modul import Modul
from Model.semester import Semester
from Model.studiengang import Studiengang


class ModulRepositoryAbstract(ABC):
    @abstractmethod
    def speichern(self, modul: Modul) -> None:
        pass

    @abstractmethod
    def lade_modul(self, modulcode : str) -> Modul:
        pass

    @abstractmethod
    def lade_alle(self) -> list[Modul]:
        pass

    @abstractmethod
    def lade_module_von_studiengang(self, studiengang: Studiengang) -> list[Modul]:
        pass

    @abstractmethod
    def lade_module_von_semester(self, semester: Semester) -> list[Modul]:
        pass

    @abstractmethod
    def aktualisieren(
        self, modul: Modul, modulname_neu: str | None = None,
        modulcode_neu: str | None = None, ects_neu: int | None = None,
        semester_neu: Semester | int | None = None,
    ) -> None:
        pass

    @abstractmethod
    def loeschen(self, modulcode: str) -> None:
        pass
