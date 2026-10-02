from Model.pruefungsleistung import Pruefungsleistung
from Model.status import Status
from Model.student import Student
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository
from Repository.sqlite_repository.sqlite_modul_repository import SQLiteModulRepository
from Repository.sqlite_repository.sqlite_student_repository import SQLiteStudentRepository


class SQLitePruefungsleistungRepository(SQLiteRepository, PruefungsleistungRepositoryAbstract):
    def __init__(self, database: Database):
        super().__init__(database)
        self.student_repository = None
        self.modul_repository = None

    def _schluessel(self, pruefungsleistung: Pruefungsleistung) -> dict:
        if pruefungsleistung.student is None:
            raise ValueError("Eine gespeicherte Prüfungsleistung benötigt einen Studenten.")
        return {
            "student_id": self.student_repository.lade_student_id(pruefungsleistung.student),
            "modul_id": self.modul_repository.lade_modul_id(pruefungsleistung.modul),
        }

    def speichern(self, pruefungsleistung: Pruefungsleistung) -> None:
        student_id = self.student_repository.lade_student_id(pruefungsleistung.student.matrikelnummer)
        modul_id = self.modul_repository.lade_modul_id(pruefungsleistung.modul.modulcode)
        self._schreiben(
            """INSERT INTO Pruefungsleistung (student_id, modul_id, note, status)
               VALUES (?, ?, ?, ?)""",
            (student_id, modul_id, pruefungsleistung.note, pruefungsleistung.status.value)
        )

    def lade_pruefungsleistung(self, pruefungsleistung: Pruefungsleistung) -> Pruefungsleistung:
        return self.from_database(self._lade_eine_zeile(
            """SELECT * FROM Pruefungsleistung
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self._schluessel(pruefungsleistung),
        ))

    def lade_von_id(self, id: int) -> Pruefungsleistung:
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Pruefungsleistung WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Pruefungsleistung]:
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Pruefungsleistung ORDER BY student_id, modul_id"
        )]

    def lade_pruefungsleistung_von_student(self, student: Student) -> list[Pruefungsleistung]:
        student_id = self.student_repository.lade_student_id(student.matrikelnummer)
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Pruefungsleistung WHERE student_id = ?", (student_id,),
        )]

    def aktualisieren(self, pruefungsleistung: Pruefungsleistung) -> None:
        self._schreiben(
            """UPDATE Pruefungsleistung SET note = :note, status = :status
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self.to_database(pruefungsleistung), muss_existieren=True,
        )

    def loeschen(self, pruefungsleistung: Pruefungsleistung) -> None:
        self._schreiben(
            """DELETE FROM Pruefungsleistung
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self._schluessel(pruefungsleistung), muss_existieren=True,
        )

    def loesche_pruefungsleistungen_von_student(self, student: Student) -> None:
        student_id = self.student_repository.lade_student_id(student.matrikelnummer)
        self._schreiben(
            """DELETE FROM Pruefungsleistung
               WHERE student_id = ?""",
            (student_id,)
        )

    def from_database(self, row) -> Pruefungsleistung:
        return Pruefungsleistung(
            student=self.student_repository.lade_von_id(row["student_id"]),
            modul=self.modul_repository.lade_von_id(row["modul_id"]),
            note=row["note"], status=Status(row["status"]),
        )

    def to_database(self, pruefungsleistung: Pruefungsleistung) -> dict:
        return {
            **self._schluessel(pruefungsleistung),
            "note": pruefungsleistung.note,
            "status": pruefungsleistung.status.value,
        }
