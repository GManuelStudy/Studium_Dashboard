from abc import ABC, abstractmethod
from Model.modul import Modul
from Model.semester import Semester
from Model.studiengang import Studiengang

class ModulRepositoryAbstract(ABC):
    """Repository Abstract mit grundlegenden CRUD-Funktionen"""
    @abstractmethod
    def speichern(self, modul: Modul) -> None:
        """Speichert ein Modul"""
        pass

    @abstractmethod
    def lade_modul(self, modulcode : str, studiengang: Studiengang | None = None) -> Modul:
        """Lade Modul nach Modulcode; bei mehrfachen Codes ist studiengang erforderlich."""
        pass

    @abstractmethod
    def lade_alle(self) -> list[Modul]:
        """Lade alle Module"""
        pass

    @abstractmethod
    def lade_module_von_studiengang(self, studiengang: Studiengang) -> list[Modul]:
        """Lade alle Module eines Studiengangs"""
        pass

    @abstractmethod
    def lade_module_von_semester(self, semester: Semester) -> list[Modul]:
        """Lade Semestermodule, sortiert nach Modulcode."""
        pass

    @abstractmethod
    def aktualisieren(
        self, modul: Modul, modulname_neu: str | None = None,
        modulcode_neu: str | None = None, ects_neu: int | None = None,
        semester_neu: Semester | int | None = None,
    ) -> None:
        """Aktualisiert Module; None behält den jeweiligen bisherigen Wert bei."""
        pass

    @abstractmethod
    def loeschen(self, modulcode: str, studiengang: Studiengang | None = None) -> None:
        """Löscht ein Modul.
        Bei mehrfach verwendetem Code ist der Studiengang erforderlich.
        """
        pass
