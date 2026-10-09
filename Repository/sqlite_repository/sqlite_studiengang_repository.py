from Model.studiengang import Studiengang
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository
from Repository.database import Database

class SQLiteStudiengangRepository(SQLiteRepository, StudiengangRepositoryAbstract):
    """Implementiert konkrete SQLite-Klasse und Mapping für das Domain-Modell"""
    def __init__(self, database: Database):
        """Initalisiert benötigte Repositories"""
        super().__init__(database)

    def speichern(self, studiengang: Studiengang) -> Studiengang:
        """Speichert ein Studiengang in der Datenbank"""
        row_id = self._schreiben(
            "INSERT INTO Studiengang (bezeichnung) VALUES (:bezeichnung)",
            self.to_database(studiengang),
        )
        studiengang = self.lade_von_id(row_id)
        return studiengang

    def lade_studiengang_id(self, studiengang: Studiengang) -> int:
        """Lade Studiengang ID"""
        return self._lade_eine_zeile(
            "SELECT id FROM Studiengang WHERE bezeichnung = ?",
            (studiengang.studiengang,),
        )["id"]

    def lade_studiengang_von_student(self, matrikelnummer: str) -> Studiengang:
        """Lade Studiengang eines Studenten"""
        return self.lade_von_id(self._lade_eine_zeile(
            "SELECT studiengang_id FROM Student WHERE matrikelnummer = ?",
            (matrikelnummer,),
        )["studiengang_id"])

    def lade_studiengang(self, studiengang: Studiengang) -> Studiengang:
        """Lade Studiengang aus Datenbank"""
        return self.lade_von_id(self.lade_studiengang_id(studiengang))

    def lade_von_id(self, id: int) -> Studiengang:
        """Lade Studiengang aus Datenbank nach technischer Datenbank-ID"""
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Studiengang WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Studiengang]:
        """Lade alle Studiengänge sortiert nach Bezeichnung"""
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Studiengang ORDER BY bezeichnung"
        )]

    def aktualisieren(self, studiengang: Studiengang, bezeichnung_neu: str) -> None:
        """Aktualisiert ein Studiengang"""
        self._schreiben(
            "UPDATE Studiengang SET bezeichnung = ? WHERE bezeichnung = ?",
            (bezeichnung_neu, studiengang.studiengang),
        )
        studiengang.studiengang = bezeichnung_neu

    def loeschen(self, studiengang: Studiengang) -> None:
        """Löscht ein Studiengang"""
        self._schreiben(
            "DELETE FROM Studiengang WHERE bezeichnung = ?",
            (studiengang.studiengang,),
        )

    def from_database(self, row) -> Studiengang:
        """Erzeugt ein Modell aus einer zur Repository-Abfrage"""
        return Studiengang(studiengang=row["bezeichnung"])

    def to_database(self, studiengang: Studiengang) -> dict:
        """Bildet das Modell auf SQL-Parameter ab und löst erforderliche Referenzen auf."""
        return {"bezeichnung": studiengang.studiengang}
