from Model.modul import Modul
from Model.semester import Semester
from Model.studiengang import Studiengang
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract

class SQLiteModulRepository(SQLiteRepository, ModulRepositoryAbstract):
    """Implementiert konkrete SQLite-Klasse und Mapping für das Domain-Modell"""
    def __init__(self, database: Database, studiengang_repository:StudiengangRepositoryAbstract):
        """Initalisiert benötigte Repositories"""
        super().__init__(database)
        self.studiengang_repository = studiengang_repository
        self.semester_repository = None

    def speichern(self, modul: Modul) -> None:
        """Speichert ein Modul in der Datenbank"""
        self._schreiben(
            """INSERT INTO Modul (modulname, modulcode, ects, semester_id, studiengang_id)
               VALUES (:modulname, :modulcode, :ects, :semester_id, :studiengang_id)""",
            self._to_database(modul),
        )

    def lade_modul_id(self, modulcode: str, studiengang: Studiengang | None = None) -> int:
        if studiengang is not None:
            studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
            return self._lade_eine_zeile(
                "SELECT id FROM Modul WHERE modulcode = ? AND studiengang_id = ?", (modulcode, studiengang_id),
            )["id"]
        return self._lade_eine_zeile(
            "SELECT id FROM Modul WHERE modulcode = ?", (modulcode,),
        )


    def lade_modul(self, modulcode: str, studiengang: Studiengang | None = None) -> Modul:
        """Lade ein Modul nach Modulcode. Bei mehrfachen Modulcodes ist studiengang erforderlich."""
        return self.lade_von_id(self.lade_modul_id(modulcode, studiengang))

    def lade_von_id(self, id: int) -> Modul:
        """Lade ein Modul nach technischer Datenbank-ID"""
        return self._from_database(self._lade_eine_zeile(
            "SELECT * FROM Modul WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Modul]:
        """Lade alle Module sortiert nach Modulcode"""
        return [self._from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Modul ORDER BY modulcode"
        )]

    def lade_module_von_studiengang(self, studiengang: Studiengang) -> list[Modul]:
        """Lade alle Module inkl. Semester eines Studiengangs sortiert nach Modulcode"""
        studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
        return [self._from_database(row) for row in self._lade_zeilen(
            """SELECT * FROM modul m 
            JOIN Semester s ON m.semester_id = s.id 
            WHERE s.studiengang_id = ? ORDER BY s.semester""",
            (studiengang_id,),
        )]

    def lade_module_von_semester(self, semester: Semester) -> list[Modul]:
        """Lade alle Module eines Semesters sortiert nach Modulcode"""
        semeser_id = self.semester_repository.lade_semester_id(semester)
        data = self._lade_zeilen(
            "SELECT * FROM modul WHERE semester_id = ?",
            (semeser_id,),
        )
        return [self._from_database(row) for row in data]

    def loeschen(self, modulcode: str, studiengang: Studiengang | None = None) -> None:
        """Löscht ein Modul. Bei mehrfach verwendetem Modulcode ist der Studiengang erforderlich."""
        if studiengang is not None:
            studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
            self._schreiben(
                "DELETE FROM Modul WHERE modulcode = ? AND studiengang_id = ?", (modulcode, studiengang_id)
            )
        else:
            return None

    def _from_database(self, row) -> Modul:
        """Erzeugt ein Modell aus einer zur Repository-Abfrage"""
        return Modul(
            modulname=row["modulname"], modulcode=row["modulcode"], ects=row["ects"],
            semester=self.semester_repository.lade_von_id(row["semester_id"]),
        )

    def _to_database(self, modul: Modul) -> dict:
        """Bildet das Modell auf SQL-Parameter ab und löst erforderliche Referenzen auf."""
        return {
            "modulname": modul.modulname, "modulcode": modul.modulcode, "ects": modul.ects,
            "semester_id": self.semester_repository.lade_semester_id(modul.semester),
            "studiengang_id": self.studiengang_repository.lade_studiengang_id(modul.semester.studiengang),
        }
