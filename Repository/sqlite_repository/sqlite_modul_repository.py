from Model.modul import Modul
from Model.semester import Semester
from Model.studiengang import Studiengang
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract


class SQLiteModulRepository(SQLiteRepository, ModulRepositoryAbstract):
    def __init__(self, database: Database, studiengang_repository:StudiengangRepositoryAbstract):
        super().__init__(database)
        self.studiengang_repository = studiengang_repository
        self.semester_repository = None

    def speichern(self, modul: Modul) -> None:
        self._schreiben(
            """INSERT INTO Modul (modulname, modulcode, ects, semester_id)
               VALUES (:modulname, :modulcode, :ects, :semester_id)""",
            self.to_database(modul),
        )

    def lade_modul_id(self, modulcode: str) -> int:
        return self._lade_eine_zeile(
            "SELECT id FROM Modul WHERE modulcode = ?", (modulcode,),
        )["id"]

    def lade_modul(self, modulcode: str) -> Modul:
        return self.lade_von_id(self.lade_modul_id(modulcode))

    def lade_von_id(self, id: int) -> Modul:
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Modul WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Modul]:
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Modul ORDER BY modulcode"
        )]

    def lade_module_von_studiengang(self, studiengang: Studiengang) -> list[Modul]:
        studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM modul m JOIN Semester s ON m.semester_id = s.id WHERE s.studiengang_id = ? ORDER BY s.semester",
            (studiengang_id,),
        )]

    def lade_module_von_semester(self, semester: Semester) -> list[Modul]:
        semeser_id = self.semester_repository.lade_semester_id(semester)
        data = self._lade_zeilen(
            "SELECT * FROM modul WHERE semester_id = ?",
            (semeser_id,),
        )
        return [self.from_database(row) for row in data]

    def aktualisieren(
        self, modul: Modul, modulname_neu: str | None = None,
        modulcode_neu: str | None = None, ects_neu: int | None = None,
        semester_neu: Semester | int | None = None,
    ) -> None:
        zielsemester = modul.semester
        if isinstance(semester_neu, int):
            zielsemester = self.semester_repository.lade_semester(Semester(
                semester_neu, modul.semester.status, modul.semester.studiengang
            ))
        elif semester_neu is not None:
            zielsemester = semester_neu
        neu = Modul(
            modul.modulname if modulname_neu is None else modulname_neu,
            modul.modulcode if modulcode_neu is None else modulcode_neu,
            modul.ects if ects_neu is None else ects_neu,
            zielsemester,
        )
        daten = self.to_database(neu)
        daten["modulcode_alt"] = modul.modulcode
        self._schreiben(
            """UPDATE Modul SET modulname = :modulname, modulcode = :modulcode,
               ects = :ects, semester_id = :semester_id WHERE modulcode = :modulcode_alt""",
            daten, muss_existieren=True,
        )
        modul.modulname, modul.modulcode, modul.ects, modul.semester = (
            neu.modulname, neu.modulcode, neu.ects, neu.semester
        )

    def loeschen(self, modulcode: str) -> None:
        self._schreiben(
            "DELETE FROM Modul WHERE modulcode = ?", (modulcode,), muss_existieren=True,
        )

    def from_database(self, row) -> Modul:
        return Modul(
            modulname=row["modulname"], modulcode=row["modulcode"], ects=row["ects"],
            semester=self.semester_repository.lade_von_id(row["semester_id"]),
        )

    def to_database(self, modul: Modul) -> dict:
        return {
            "modulname": modul.modulname, "modulcode": modul.modulcode, "ects": modul.ects,
            "semester_id": self.semester_repository.lade_semester_id(modul.semester),
        }
