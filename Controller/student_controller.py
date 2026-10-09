from Model.pruefungsleistung import Pruefungsleistung
from Model.status import Status
from Model.student import Student
from Model.studiengang import Studiengang
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
import datetime

class StudentController:
    """Übernimmt Aufgaben der Studenten-Views und koordiniert Speichervorgänge."""
    def __init__(
            self,
            student_repository: StudentRepositoryAbstract,
            modul_repository: ModulRepositoryAbstract,
            pruefungsleistung_repository: PruefungsleistungRepositoryAbstract
    ) -> None:
        """Initialisiert StudentController und erstellt Abhängigkeiten"""
        self._student_rep = student_repository
        self._modul_rep = modul_repository
        self._pruefungsleistung_rep = pruefungsleistung_repository

    def lade_alle_studenten(self) -> list[Student]:
        """Lade alle Studenten aus Repository"""
        return self._student_rep.lade_alle()

    def lade_student(self, matrikelnummer: str) -> tuple[Student | None, str | None]:
        """Lade Student inklusiver Prüfungsleistungen aus Repository.
        Rückgabe: (Student, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        try:
            student = self._student_rep.lade_student(matrikelnummer)
            pruefungsleistungen = self._pruefungsleistung_rep.lade_pruefungsleistung_von_student(student)
            for pruefungsleistung in pruefungsleistungen:
                student.pruefungsleistungen.append(pruefungsleistung)
        except TypeError:
            return None, "Student wurde nicht gefunden."
        return student, None

    def student_hinzufuegen(
            self,
            vorname: str,
            nachname: str,
            matrikelnummer: str,
            studiengang: Studiengang,
            notendurchschnitt_ziel: float,
            beginndatum: datetime,
            zielabschlussdatum: datetime
    ) -> tuple[Student | None, str | None]:
        """Erstellt Studenten-Objekt und speichert in Datenbank.
        Legt Pruefungsleistungen für Studenten an.
        Rückgabe: (Student, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        student = Student(
            vorname, nachname, matrikelnummer, studiengang,
            notendurchschnitt_ziel, beginndatum, zielabschlussdatum
        )
        try:
            self._student_rep.speichern(student)

            module = self._modul_rep.lade_module_von_studiengang(student.studiengang)
            for modul in module:
                pruefungsleistung = Pruefungsleistung(student, modul, None, Status.OFFEN)
                self._pruefungsleistung_rep.speichern(pruefungsleistung, student.studiengang)
                student.pruefungsleistungen.append(pruefungsleistung)
        except ValueError:
            return None, "Der Student existiert bereits."
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."
        return student, None

    def student_aktualisieren(
            self,
            student: Student,
            vorname: str,
            nachname: str,
            matrikelnummer: str,
            studiengang: Studiengang,
            notendurchschnitt_goal: float,
            beginndatum: datetime,
            zielabschlussdatum: datetime
    ) -> tuple[Student | None, str | None]:
        """Aktualisiert Studenten-Objekt und speichert in Datenbank
        Bei geänderten Studiengang werden alte Pruefungsleistungen gelöscht und neue angelegt.
        Rückgabe: (Student, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        studiengang_check = student.studiengang.studiengang != studiengang.studiengang
        try:
            if studiengang_check:
                if student.pruefungsleistungen:
                    self._pruefungsleistung_rep.loesche_pruefungsleistungen_von_student(student)
                    student.pruefungsleistungen.clear()
                module = self._modul_rep.lade_module_von_studiengang(studiengang)
                if module:
                    for modul in module:
                        pruefungsleistung = Pruefungsleistung(student, modul, None, Status.OFFEN)
                        self._pruefungsleistung_rep.speichern(pruefungsleistung, studiengang)
                        student.pruefungsleistungen.append(pruefungsleistung)

            self._student_rep.aktualisieren(
                student,
                vorname,
                nachname,
                matrikelnummer,
                studiengang,
                notendurchschnitt_goal,
                beginndatum,
                zielabschlussdatum
            )
        except ValueError:
            return None, "Der Student existiert bereits."
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."
        return student, None

    def student_loeschen(self, matrikelnummer: str):
        """Loescht Student aus Datenbank"""
        try:
            self._student_rep.loeschen(matrikelnummer)
        except TypeError:
            return None, "Student existiert nicht."

    def pruefungsleistungen_aktualisieren(
            self,
            student,
            data
    ) -> tuple[Pruefungsleistung | str | None, str | None]:
        """Lest Daten aus dem Sheet. Speichert eingetragene Note und berechnet Status.
        Pruefungsleistungen werden in der Datenbank aktualisiert.
        Rückgabe: (Pruefungsleistung, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        for pruefungsleistung, row in zip(student.pruefungsleistungen, data):
            # Prüft ob Note leer ist. Wenn ja, wird Note auf 0 gesetzt
            if row[4] == '':
                row[4] = 0
            try:
                note = float(row[4])
            except ValueError:
                note = 0

            pruefungsleistung.note = note

            # Berechnet Status basierend auf Note
            if note > 4:
                status = Status.NICHT_BESTANDEN
            elif note == 0:
                status = Status.OFFEN
                pruefungsleistung.note = None
            else:
                status = Status.ABGESCHLOSSEN

            pruefungsleistung.status = status
            try:
                pruefungsleistung = self._pruefungsleistung_rep.aktualisieren(pruefungsleistung)
            except TypeError:
                return None, "Student existiert nicht."
            except:
                return None, "Ein unerwarteter Fehler ist aufgetreten."

        return '', None
