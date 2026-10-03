from Model import pruefungsleistung
from Model.pruefungsleistung import Pruefungsleistung
from Model.status import Status
from Model.student import Student
from Model.studiengang import Studiengang
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
import datetime

class StudentController:
    def __init__(self, student_repository: StudentRepositoryAbstract, modul_repository: ModulRepositoryAbstract, pruefungsleistung_repository: PruefungsleistungRepositoryAbstract) -> None:
        self._student_rep = student_repository
        self._modul_rep = modul_repository
        self._pruefungsleistung_rep = pruefungsleistung_repository

    def get_studenten(self):
        return self._student_rep.lade_alle()

    def get_student(self, matrikelnummer: str) -> Student:
        student = self._student_rep.lade_student(matrikelnummer)
        pruefungsleistungen = self._pruefungsleistung_rep.lade_pruefungsleistung_von_student(student)
        for pruefungsleistung in pruefungsleistungen:
            student.pruefungsleistungen.append(pruefungsleistung)
        return student

    def add_student(self, vorname: str, nachname: str, matrikelnummer: str, studiengang: Studiengang, notendurchschnitt_ziel: float, beginndatum: datetime, zielabschlussdatum: datetime):

        if zielabschlussdatum <= beginndatum:
            # ende ist vor dem beginn
            # TODO: Fehlermeldung anzeigen
            return
        student = Student(vorname, nachname, matrikelnummer, studiengang, notendurchschnitt_ziel, beginndatum, zielabschlussdatum)
        self._student_rep.speichern(student)
        module = self._modul_rep.lade_module_von_studiengang(student.studiengang)
        for modul in module:
            pruefungsleistung = Pruefungsleistung(student, modul, None, Status.OFFEN)
            self._pruefungsleistung_rep.speichern(pruefungsleistung)
            student.pruefungsleistungen.append(pruefungsleistung)

    def update_student(self, student:Student, vorname: str, nachname: str, matrikelnummer: str, studiengang: Studiengang, notendurchschnitt_goal: float, beginndatum: datetime, zielabschlussdatum: datetime):
        if zielabschlussdatum <= beginndatum:
            return
        studiengang_check = student.studiengang.studiengang != studiengang.studiengang

        if studiengang_check:
            self._pruefungsleistung_rep.loesche_pruefungsleistungen_von_student(student)
            module = self._modul_rep.lade_module_von_studiengang(studiengang)
            student.pruefungsleistungen.clear()
            for modul in module:
                pruefungsleistung = Pruefungsleistung(student, modul, None, Status.OFFEN)
                self._pruefungsleistung_rep.speichern(pruefungsleistung)
                student.pruefungsleistungen.append(pruefungsleistung)

        self._student_rep.aktualisieren(student, vorname, nachname, matrikelnummer, studiengang, notendurchschnitt_goal, beginndatum, zielabschlussdatum)

    def del_student(self, matrikelnummer: str):
        self._student_rep.loeschen(matrikelnummer)

    def update_pruefungsleistungen(self, student, data):
        for pruefungsleistung, row in zip(student.pruefungsleistungen, data):
            if row[4] == '':
                row[4] = 0


            note = float(row[4])

            pruefungsleistung.note = note

            if note == 5:
                status = Status.NICHT_BESTANDEN
            elif note == 0:
                status = Status.OFFEN
                pruefungsleistung.note = None
            else:
                status = Status.ABGESCHLOSSEN

            pruefungsleistung.status = status
            self._pruefungsleistung_rep.aktualisieren(pruefungsleistung)