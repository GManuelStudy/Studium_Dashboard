from Model.modul import Modul
from Model.pruefungsleistung import Pruefungsleistung
from Model.semester import Semester
from Model.status import Status
from Model.student import Student
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DashboardService:
    """Berechnet Kennzahlen der Dashboard-Daten"""
    def berechne_semester_notendurchschnitt(self, semester: Semester, student: Student) -> float:
        """Berechnet Notendurchschnitt eines Semesters anhand benoteter Prüfungsleistungen
        Sind keine Noten vorhanden, wird 0 zurückgegeben.
        """
        noten = [pruefung.note for pruefung in student.pruefungsleistungen
                 if pruefung.modul.semester.semester == semester.semester and
                 pruefung.note is not None
                 ]
        if len(noten) == 0:
            return 0
        return sum(noten) / len(noten)

    def berechne_semester_status(self, semester: Semester, student: Student) -> Status:
        """Berechnet Semester-Status anhand abgeschlossener Module innerhalb eines Semesters.
        Unvollständige Semester sind Status.OFFEN.
        Status.ABGESCHLOSSEN gilt nur, wenn alle Module abgeschlossen sind.
        Ist ein Modul nicht bestanden, so gilt das ganze Semester als Status.NICHT_BESTANDEN.
        """
        module = {modul.modulcode for modul in semester.module}
        pruefungsleistungen = [item for item in student.pruefungsleistungen if item.modul.modulcode in module]

        if not pruefungsleistungen:
            return Status.OFFEN

        if any(item.status == Status.NICHT_BESTANDEN for item in pruefungsleistungen):
            return Status.NICHT_BESTANDEN

        if all(item.status == Status.ABGESCHLOSSEN for item in pruefungsleistungen):
            return Status.ABGESCHLOSSEN

        return Status.OFFEN

    def berechne_erforderliche_note(self, student: Student) -> tuple[float, float]:
        """Berechnet erforderliche Note anhand aktueller Notendurchschnitt und Zielnotendurchschnitt.
        Gibt die erforderliche Note und den dadurch erreichten neuen Notendurchschnitt zurück.
        Rückgabe: tupel (benoetigte_note als float, durchschnitt_neu als float)
        """
        anzahl_pruefungen = len([
            item for item in student.pruefungsleistungen
            if item.status != Status.OFFEN and item.note is not None
        ])
        # Ist benoetigte_note < 1, so ist der zielnotendurchschnitt mit einer note nicht zu erreichen.
        # Somit wird benoetigte_note auf 1 gesetzt.
        benoetigte_note = max(
            student.zielnotendurchschnitt * (anzahl_pruefungen + 1) -
            student.aktuellerNotendurchschnitt * anzahl_pruefungen, 1.0
        )
        durchschnitt_neu = max(
            (student.aktuellerNotendurchschnitt * anzahl_pruefungen + benoetigte_note) /
            (anzahl_pruefungen + 1), 1.0
        )
        return benoetigte_note, durchschnitt_neu

    def berechne_studienfortschritt(self, student: Student) -> float:
        """Berechnet Studienfortschritt anhand aktueller ECTS und GesamtECTS.
        Gibt den studienfortschritt als float zurück.
        """
        if student.studiengang.ectsGesamt == 0:
            return 0
        return student.aktuelleECTS / student.studiengang.ectsGesamt * 100

    def berechne_verbleibende_dauer(self, student: Student) -> relativedelta:
        """Berechnet Verbleibende Studiendauer anhand des Zielabschlussdatums.
        Gibt die verbleibende Dauer als relativedelta zurück.
        """
        if student.zielabschlussdatum < datetime.now():
            return relativedelta(None)
        return relativedelta(student.zielabschlussdatum, datetime.now())

    def berechne_verfuegbare_dauer_pro_modul(self, student: Student) -> float | None:
        """Berechnet durchschnittlich verfügbare Dauer pro Modul anhand des Zielabschlussdatums und den offenen Modulen.
        Gibt die Tage zurück, die pro Modul verfügbar sind.
        """
        anzahl_module_offen = len([item for item in student.pruefungsleistungen if item.status == Status.OFFEN])

        if anzahl_module_offen < 1:
            return None
        if student.zielabschlussdatum < datetime.now():
            return None

        verbleibende_dauer = (student.zielabschlussdatum - datetime.now()).days
        tage_pro_modul = verbleibende_dauer / anzahl_module_offen
        return tage_pro_modul

    def berechne_studiendauer_fortschritt(self, student: Student) -> float:
        """Berechnet Studiendauer Fortschritt anhand des Zielabschlussdatums und gesamten Studiendauer.
        Gibt die studiendauer_fortschritt als float zurück.
        """
        datum_heute = datetime.now()

        if datum_heute < student.beginndatum:
            return 0
        if datum_heute >= student.zielabschlussdatum:
            return 100

        dauer_ges = (student.zielabschlussdatum - student.beginndatum).total_seconds()
        dauer_vergangen = (datum_heute - student.beginndatum).total_seconds()
        return dauer_vergangen / dauer_ges * 100

    def get_pruefungsleistung(self, student: Student, modul: Modul) -> Pruefungsleistung | None:
        """Bekommt eine Prüfungsleistung nach Student und Modulcode."""
        return next(
            (item for item in student.pruefungsleistungen
             if item.modul.modulcode == modul.modulcode), None
        )
