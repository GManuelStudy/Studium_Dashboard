from datetime import datetime
from Model.student import Student
from Model.studiengang import Studiengang
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Repository.database import Database
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository

class SQLiteStudentRepository(SQLiteRepository, StudentRepositoryAbstract):
    """Implementiert konkrete SQLite-Klasse und Mapping für das Domain-Modell"""
    def __init__(self, database: Database, studiengang_repository: StudiengangRepositoryAbstract):
        """Initalisiert benötigte Repositories"""
        super().__init__(database)
        self.studiengang_repository = studiengang_repository

    def speichern(self, student: Student) -> None:
        """Speichert ein Student in der Datenbank"""
        self._schreiben(
            """INSERT INTO Student (vorname, nachname, matrikelnummer, studiengang_id,
               zielnotendurchschnitt, beginndatum, zielabschlussdatum)
               VALUES (:vorname, :nachname, :matrikelnummer, :studiengang_id,
               :zielnotendurchschnitt, :beginndatum, :zielabschlussdatum)""",
            self._to_database(student),
        )

    def lade_student_id(self, matrikelnummer: str) -> int:
        """Lade Student ID"""
        return self._lade_eine_zeile(
            "SELECT id FROM Student WHERE matrikelnummer = ?", (matrikelnummer,),
        )["id"]

    def lade_student(self, matrikelnummer: str) -> Student:
        """Lade Student aus Datenbank"""
        return self.lade_von_id(self.lade_student_id(matrikelnummer))

    def lade_von_id(self, id: int) -> Student:
        """Lade Student aus Datenbank nach technischer Datenbank-ID"""
        return self._from_database(self._lade_eine_zeile(
            "SELECT * FROM Student WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Student]:
        """Lade alle Studenten sortiert nach Matrikelnummer"""
        studenten = []

        for row in self._lade_zeilen("SELECT * FROM Student ORDER BY matrikelnummer"):
            try:
                student = self._from_database(row)
                studenten.append(student)

            except TypeError:
                self.loeschen(row["matrikelnummer"])

        return studenten

    def lade_alle_von_studiengang(self, studiengang: Studiengang) -> list[Student]:
        """Lade alle Studenten eines Studiengangs sortiert nach Matrikelnummer"""
        studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
        return [self._from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Student WHERE studiengang_id = ? ORDER BY matrikelnummer",
            (studiengang_id,),
        )]

    def aktualisieren(
            self,
            student: Student,
            vorname_neu:str,
            nachname_neu:str,
            matrikelnummer_neu:str,
            studiengang: Studiengang,
            notendurchschnitt_ziel:float,
            beginndatum_neu: datetime,
            zielabschlussdatum_neu: datetime
    ) -> None:
        """Aktualisiert ein Student"""
        studiengang_id = self.studiengang_repository.lade_studiengang_id(studiengang)
        self._schreiben(
            """UPDATE Student SET vorname = ?, nachname = ?, matrikelnummer = ?,
               studiengang_id = ?, zielnotendurchschnitt = ?,
               beginndatum = ?, zielabschlussdatum = ?
               WHERE matrikelnummer = ?""",
            (
                vorname_neu,
                nachname_neu,
                matrikelnummer_neu,
                studiengang_id,
                notendurchschnitt_ziel,
                beginndatum_neu,
                zielabschlussdatum_neu,
                student.matrikelnummer,
            )
        )

    def loeschen(self, matrikelnummer: str) -> None:
        """Löscht ein Student aus der Datenbank"""
        self._schreiben(
            "DELETE FROM Student WHERE matrikelnummer = ?",
            (matrikelnummer,),
        )

    def _from_database(self, row) -> Student:
        """Erzeugt ein Modell aus einer zur Repository-Abfrage"""
        return Student(
            vorname=row["vorname"], nachname=row["nachname"], matrikelnummer=row["matrikelnummer"],
            studiengang=self.studiengang_repository.lade_von_id(row["studiengang_id"]),
            zielnotendurchschnitt=row["zielnotendurchschnitt"],
            beginndatum=datetime.fromisoformat(row["beginndatum"]),
            zielabschlussdatum=datetime.fromisoformat(row["zielabschlussdatum"]),
        )

    def _to_database(self, student: Student) -> dict:
        """Bildet das Modell auf SQL-Parameter ab und löst erforderliche Referenzen auf."""
        return {
            "vorname": student.vorname, "nachname": student.nachname,
            "matrikelnummer": student.matrikelnummer,
            "studiengang_id": self.studiengang_repository.lade_studiengang_id(student.studiengang),
            "zielnotendurchschnitt": student.zielnotendurchschnitt,
            "beginndatum": student.beginndatum.isoformat() if student.beginndatum is not None else None,
            "zielabschlussdatum": student.zielabschlussdatum.isoformat() if student.zielabschlussdatum is not None else None,
        }
