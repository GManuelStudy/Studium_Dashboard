from Model.modul import Modul
from Model.pruefungsleistung import Pruefungsleistung
from Model.studiengang import Studiengang
from Model.semester import Semester
from Model.status import Status
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.semester_repository_abstract import SemesterRepositoryAbstract

class StudiengangController:
    """Übernimmt Aufgaben der Studiengang-Views und koordiniert Speichervorgänge."""
    def __init__(
            self,
            studiengang_repository: StudiengangRepositoryAbstract,
            modul_repositoy: ModulRepositoryAbstract,
            semester_repository: SemesterRepositoryAbstract,
            student_repository: StudentRepositoryAbstract,
            pruefungsleistung_repository: PruefungsleistungRepositoryAbstract
    ) -> None:
        """Initialisiert StudiengangController mit benötigten Abhängigkeiten"""
        self._studiengang_rep = studiengang_repository
        self._modul_rep = modul_repositoy
        self._semester_rep = semester_repository
        self._student_rep = student_repository
        self._pruefungsleistung_rep = pruefungsleistung_repository

    def lade_alle_studiengaenge(self) -> list[Studiengang]:
        """Lade Studiengang inklusive Semester und Module von Repository."""
        studiengaenge_temp = self._studiengang_rep.lade_alle()
        studiengaenge = []

        for studiengang in studiengaenge_temp:
            studiengang.semester = self._semester_rep.lade_semester_von_studiengang(studiengang)
            for semester in studiengang.semester:
                semester.module = self._modul_rep.lade_module_von_semester(semester)
            studiengaenge.append(studiengang)

        return studiengaenge

    def lade_studiengang(self, bezeichnung: str) -> tuple[Studiengang | None, str | None]:
        """Lade Studiengang von Repository.
        Rückgabe: (Studiengang, None) bei Erfolg; (None, str) als Fehlermeldung"""
        studiengang_temp = Studiengang(studiengang=bezeichnung)
        try:
            studiengang = self._studiengang_rep.lade_studiengang(studiengang_temp)
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        return studiengang, None

    def studiengang_hinzufuegen(self, bezeichnung: str) -> tuple[Studiengang | None, str | None]:
        """Erstellt Studiengang-Objekt und speichert in Datenbank.
        Rückgabe: (Studiengang, None) bei Erfolg; (None, str) als Fehlermeldung"""
        bezeichnung = bezeichnung.strip()
        studiengang = Studiengang(studiengang=bezeichnung)

        try:
            studiengang_neu = self._studiengang_rep.speichern(studiengang)
        except ValueError:
            return None, "Der Studiengang existiert bereits."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        return studiengang_neu, None

    def studiengang_aktualisieren(
            self,
            studiengang: Studiengang,
            bezeichnung_neu: str
    ) -> tuple[Studiengang | None, str | None]:
        """Aktualisiert Studiengang-Objekt und speichert in Datenbank.
        Rückgabe: (Studiengang, None) bei Erfolg; (None, str) als Fehlermeldung"""
        try:
            self._studiengang_rep.aktualisieren(studiengang, bezeichnung_neu)
        except ValueError:
            return None, "Der Studiengang existiert bereits."
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        return studiengang, None

    def studiengang_loeschen(self, studiengang_bez: str) -> tuple[Studiengang | None, str | None]:
        """Loesche Studiengang aus Datenbank. Prueft ob Studenten vorhanden sind.
        Rückgabe: (Student, None) bei Erfolg; (None, str) als Fehlermeldung
        """

        try:
            studiengang = Studiengang(studiengang=studiengang_bez)
            studenten = self._student_rep.lade_alle_von_studiengang(studiengang)
            if studenten:
                return None, "Studenten in diesem Studiengang sind noch vorhanden."
            self._studiengang_rep.loeschen(Studiengang(studiengang_bez))
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        return studiengang, None

    def lade_module_von_studiengang(
            self,
            studiengang: Studiengang
    ) -> tuple[list[Modul] | None, str | None]:
        """Lade Module eines Studiengangs
        Rückgabe: (Modul, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        try:
            module = self._modul_rep.lade_module_von_studiengang(studiengang)
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        return module, None

    def modul_hinzufuegen(
            self,
            modulname: str,
            modulcode: str,
            ects: int,
            semester_num: int,
            studiengang: Studiengang
    ) -> tuple[Modul | None, str | None]:
        """Erstellt Modul und speichert in Datenbank.
        Prueft ob Semester existiert. Falls nicht, wird es angelegt.
        Prueft ob Studenten in dem betroffenen Studiengang vorhanden sind. Wenn ja, werden
        Pruefungsleistungen angelegt.
        Rückgabe: (Modul, None) bei Erfolg; (None, str) als Fehlermeldung
        """
        # Validierung
        if not studiengang:
            return None, "Studiengang ist nicht vorhanden."
        if modulname.strip() == "" or modulcode.strip() == "" or ects == "" or semester_num == "":
            return None, "Alle Modul-Eingabefelder müssen befüllt sein."
        if modulname.strip() == modulcode.strip():
            return None, "Modulname und Modulcode dürfen nicht identisch sein."
        try:
            # Prueft ob Semester existiert. Falls nicht, wird es angelegt.
            semester_list = self._semester_rep.lade_semester_von_studiengang(studiengang)
            semester = next((item for item in semester_list if item.semester == int(semester_num)), None)
            if semester is None:
                semester = Semester(semester_num, studiengang)
                self._semester_rep.speichern(semester)

            modul = Modul(modulcode, modulname, ects, semester)
            self._modul_rep.speichern(modul)
        except ValueError:
            return None, f"Ein Modul mit dem Modulcode \"{modulcode}\" existiert bereits."
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        # Pruefungsleistungen anlegen, falls Studenten vorhanden sind
        try:
            self.student_list = self._student_rep.lade_alle_von_studiengang(studiengang)
            for student in self.student_list:
                pruefungsleistung = Pruefungsleistung(student, modul, None, Status.OFFEN)
                self._pruefungsleistung_rep.speichern(pruefungsleistung, studiengang)
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."

        return modul, None

    def modul_loeschen(self, modulcode: str, studiengang: Studiengang):
        """Loescht Module aus Datenbank.
        Prueft ob Semester leer ist. Falls ja, wird es geloescht.
        """
        try:
            modul = self._modul_rep.lade_modul(modulcode, studiengang)
            semester = modul.semester
            self._modul_rep.loeschen(modulcode, studiengang)
            module = self._modul_rep.lade_module_von_semester(modul.semester)
            if not module:
                self._semester_rep.loeschen(semester)
        except TypeError:
            return None, "Studiengang wurde nicht gefunden."
        except:
            return None, "Ein unerwarteter Fehler ist aufgetreten."
