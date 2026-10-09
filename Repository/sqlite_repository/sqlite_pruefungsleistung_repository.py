from Model.pruefungsleistung import Pruefungsleistung
from Model.status import Status
from Model.student import Student
from Model.studiengang import Studiengang
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository

class SQLitePruefungsleistungRepository(SQLiteRepository, PruefungsleistungRepositoryAbstract):
    """Implementiert konkrete SQLite-Klasse und Mapping für das Domain-Modell"""
    def __init__(self, database: Database):
        """Initalisiert benötigte Repositories"""
        super().__init__(database)
        self._student_repository = None
        self._modul_repository = None
        self._studiengang_repository = None

    def _schluessel(self, pruefungsleistung: Pruefungsleistung) -> dict:
        """Löst Student und Modul einer Prüfung in technische Fremdschlüssel auf.
        Ein fehlender Student erzeugt ValueError.
        """
        studiengang = self._studiengang_repository.lade_studiengang_von_student(pruefungsleistung.student.matrikelnummer)
        if pruefungsleistung.student is None:
            raise ValueError("Eine gespeicherte Prüfungsleistung benötigt einen Studenten.")
        return {
            "student_id": self._student_repository.lade_student_id(pruefungsleistung.student.matrikelnummer),
            "modul_id": self._modul_repository.lade_modul_id(pruefungsleistung.modul.modulcode, studiengang),
        }

    def speichern(self, pruefungsleistung: Pruefungsleistung, studiengang: Studiengang) -> None:
        """Speichert Prüfungsleistung in Datenbank."""
        student_id = self._student_repository.lade_student_id(pruefungsleistung.student.matrikelnummer)
        modul_id = self._modul_repository.lade_modul_id(pruefungsleistung.modul.modulcode, studiengang)
        self._schreiben(
            """INSERT INTO Pruefungsleistung (student_id, modul_id, note, status)
               VALUES (?, ?, ?, ?)""",
            (student_id, modul_id, pruefungsleistung.note, pruefungsleistung.status.value)
        )

    def lade_pruefungsleistung(self, pruefungsleistung: Pruefungsleistung) -> Pruefungsleistung:
        """Lade Prüfungsleistung aus Datenbank"""
        return self.from_database(self._lade_eine_zeile(
            """SELECT * FROM Pruefungsleistung
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self._schluessel(pruefungsleistung),
        ))

    def lade_von_id(self, id: int) -> Pruefungsleistung:
        """Lade Objekt nach technischer Datenbank-ID"""
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Pruefungsleistung WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Pruefungsleistung]:
        """Lade alle Prüfungsleistungen sortiert nach Student und Modul"""
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Pruefungsleistung ORDER BY student_id, modul_id"
        )]

    def lade_pruefungsleistung_von_student(self, student: Student) -> list[Pruefungsleistung]:
        """Lade Prüfungsleistungen eines Studenten"""
        student_id = self._student_repository.lade_student_id(student.matrikelnummer)
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Pruefungsleistung WHERE student_id = ?", (student_id,),
        )]

    def aktualisieren(self, pruefungsleistung: Pruefungsleistung) -> None:
        """Speichert Note und Status für Student-Modul-Paar"""
        self._schreiben(
            """UPDATE Pruefungsleistung SET note = :note, status = :status
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self.to_database(pruefungsleistung),
        )

    def loeschen(self, pruefungsleistung: Pruefungsleistung) -> None:
        """Löscht Prüfungsleistung"""
        self._schreiben(
            """DELETE FROM Pruefungsleistung
               WHERE student_id = :student_id AND modul_id = :modul_id""",
            self._schluessel(pruefungsleistung),
        )

    def loesche_pruefungsleistungen_von_student(self, student: Student) -> None:
        """Entfernt alle Prüfungsleistungen eines Studenten"""
        student_id = self._student_repository.lade_student_id(student.matrikelnummer)
        self._schreiben(
            """DELETE FROM Pruefungsleistung
               WHERE student_id = ?""",
            (student_id,)
        )

    def from_database(self, row) -> Pruefungsleistung:
        """Erzeugt ein Modell aus einer zur Repository-Abfrage"""
        return Pruefungsleistung(
            student=self._student_repository.lade_von_id(row["student_id"]),
            modul=self._modul_repository.lade_von_id(row["modul_id"]),
            note=row["note"], status=Status(row["status"]),
        )

    def to_database(self, pruefungsleistung: Pruefungsleistung) -> dict:
        """Bildet das Modell auf SQL-Parameter ab und löst erforderliche Referenzen auf."""
        return {
            **self._schluessel(pruefungsleistung),
            "note": pruefungsleistung.note,
            "status": pruefungsleistung.status.value,
        }
