from Model.semester import Semester
from Model.status import Status
from Model.student import Student
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DashboardService:
    def berechne_semester_notendurchschnitt(self, semester: Semester, student: Student) -> float:
        noten = [pruefung.note for pruefung in student.pruefungsleistungen
                 if pruefung.modul.semester == semester and
                 pruefung.note is not None
        ]
        return sum(noten) / len(noten)

    def berechne_erforderliche_note(self, student: Student) -> float:
        anzahl_pruefungen = len([item for item in student.pruefungsleistungen if item.status != Status.OFFEN and item.note is not None])
        benoetigte_note = student.zielnotendurchschnitt * (anzahl_pruefungen + 1) - student.aktuellerNotendurchschnitt * anzahl_pruefungen
        if benoetigte_note < 1:
            return 1
        return benoetigte_note

    def berechne_studienfortschritt(self, student: Student) -> float:
        return student.aktuelleECTS / student.studiengang.ectsGesamt * 100

    def berechne_verbleibende_dauer(self, student: Student) -> relativedelta:
        if student.zielabschlussdatum < datetime.now():
            return relativedelta(None)
        return relativedelta(student.zielabschlussdatum, datetime.now())

    def berechne_verfuegbare_dauer_pro_modul(self, student: Student) -> float| None:
        anzahl_module_offen = len([item for item in student.pruefungsleistungen if item.status == Status.OFFEN])

        if anzahl_module_offen < 1:
            return None
        if student.zielabschlussdatum < datetime.now():
            return None

        verbleibende_dauer = (student.zielabschlussdatum - datetime.now()).days
        tage_pro_modul = verbleibende_dauer / anzahl_module_offen
        return tage_pro_modul

    def berechne_studiendauer_fortschritt(self, student: Student) -> float:
        datum_heute = datetime.now()

        if datum_heute < student.beginndatum:
            return 0
        if datum_heute >= student.zielabschlussdatum:
            return 100

        dauer_ges = (student.zielabschlussdatum - student.beginndatum).total_seconds()
        dauer_vergangen = (datum_heute - student.beginndatum).total_seconds()
        return dauer_vergangen / dauer_ges * 100