from Model.studiengang import Studiengang
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Repository.sqlite_repository._sqlite_repository import SQLiteRepository


class SQLiteStudiengangRepository(SQLiteRepository, StudiengangRepositoryAbstract):

    def speichern(self, studiengang: Studiengang) -> Studiengang:
        row_id = self._schreiben(
            "INSERT INTO Studiengang (bezeichnung) VALUES (:bezeichnung)",
            self.to_database(studiengang),
        )
        studiengang = self.lade_von_id(row_id)
        return studiengang

    def lade_studiengang_id(self, studiengang: Studiengang) -> int:
        return self._lade_eine_zeile(
            "SELECT id FROM Studiengang WHERE bezeichnung = ?",
            (studiengang.studiengang,),
        )["id"]

    def lade_studiengang_von_student(self, matrikelnummer: str) -> Studiengang:
        return self.lade_von_id(self._lade_eine_zeile(
            "SELECT studiengang_id FROM Student WHERE matrikelnummer = ?",
            (matrikelnummer,),
        )["studiengang_id"])

    def lade_studiengang(self, studiengang: Studiengang) -> Studiengang:
        return self.lade_von_id(self.lade_studiengang_id(studiengang))

    def lade_von_id(self, id: int) -> Studiengang:
        return self.from_database(self._lade_eine_zeile(
            "SELECT * FROM Studiengang WHERE id = ?", (id,),
        ))

    def lade_alle(self) -> list[Studiengang]:
        return [self.from_database(row) for row in self._lade_zeilen(
            "SELECT * FROM Studiengang ORDER BY bezeichnung"
        )]

    def aktualisieren(self, studiengang: Studiengang, bezeichnung_neu: str) -> None:
        self._schreiben(
            "UPDATE Studiengang SET bezeichnung = ? WHERE bezeichnung = ?",
            (bezeichnung_neu, studiengang.studiengang), muss_existieren=True,
        )
        studiengang.studiengang = bezeichnung_neu

    def loeschen(self, studiengang: Studiengang) -> None:
        self._schreiben(
            "DELETE FROM Studiengang WHERE bezeichnung = ?",
            (studiengang.studiengang,), muss_existieren=True,
        )

    def from_database(self, row) -> Studiengang:
        return Studiengang(studiengang=row["bezeichnung"])

    def to_database(self, studiengang: Studiengang) -> dict:
        return {"bezeichnung": studiengang.studiengang}
