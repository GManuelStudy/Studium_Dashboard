from Model.semester import Semester
from Model.status import Status
from Model.studiengang import Studiengang
from Repository.abstract_repository.semester_repository_abstract import SemesterRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract


class SQLiteSemesterRepository(SQLiteRepository, SemesterRepositoryAbstract):
    def __init__(self, database: Database, studiengang_repository : StudiengangRepositoryAbstract):
        super().__init__(database)
        self.studiengang_repository = studiengang_repository
        self.modul_repository = None

    def speichern(self, semester: Semester) -> None:
        self._schreiben(
            """INSERT INTO Semester (semester, studiengang_id)
               VALUES (:semester, :studiengang_id)""",
            self.to_database(semester),
        )

    def lade_semester_id(self, semester: Semester) -> int:
        return self._lade_eine_zeile(
            "SELECT id FROM Semester WHERE semester = ? AND studiengang_id = ?",
            (semester.semester, self.studiengang_repository.lade_studiengang_id(semester.studiengang)),
        )["id"]

    def lade_semester(self, semester: Semester) -> Semester:
        return self.lade_von_id(self.lade_semester_id(semester))

    def lade_von_id(self, id: int) -> Semester:
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Semester WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Semester]:
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Semester ORDER BY studiengang_id, semester"
        )]

    def lade_semester_von_studiengang(self, studiengang: Studiengang) -> list[Semester]:
        studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Semester WHERE studiengang_id = ? ORDER BY semester",
            (studiengang_id,),
        )]

    def aktualisieren(self, semester: Semester, semester_neu: int | None = None) -> None:
        daten = self.to_database(semester)
        daten["semester_alt"] = semester.semester
        if semester_neu is not None:
            daten["semester"] = semester_neu
        self._schreiben(
            """UPDATE Semester SET semester = :semester
               WHERE semester = :semester_alt AND studiengang_id = :studiengang_id""",
            daten, muss_existieren=True,
        )
        semester.semester = daten["semester"]

    def loeschen(self, semester: Semester) -> None:
        self._schreiben(
            "DELETE FROM Semester WHERE id = ?",
            (self.lade_semester_id(semester),), muss_existieren=True,
        )

    def from_database(self, row) -> Semester:
        return Semester(
            semester=row["semester"],
            studiengang=self.studiengang_repository.lade_von_id(row["studiengang_id"]),
        )

    def to_database(self, semester: Semester) -> dict:
        return {
            "semester": semester.semester,
            "studiengang_id": self.studiengang_repository.lade_studiengang_id(semester.studiengang),
        }
