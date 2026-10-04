from DTO.modulDTO import ModulDTO
from DTO.semesterDTO import SemesterDTO
from DTO.dashboardDTO import DashboardDTO
from Model import pruefungsleistung
from Model.status import Status
from Model.student import Student
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
from Repository.abstract_repository.semester_repository_abstract import SemesterRepositoryAbstract
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Service import dashboard_service
from Service.dashboard_service import DashboardService


class DashboardController:
    def __init__(self, student_repository: StudentRepositoryAbstract, modul_repository: ModulRepositoryAbstract, pruefungsleistung_repository: PruefungsleistungRepositoryAbstract, studiengang_repository: StudiengangRepositoryAbstract, semester_repository: SemesterRepositoryAbstract, dashboardService: DashboardService) -> None:
        self._student_rep = student_repository
        self._modul_rep = modul_repository
        self._pruefungsleistung_rep = pruefungsleistung_repository
        self._studiengang_rep = studiengang_repository
        self._semester_rep = semester_repository
        self._dashboard_service = dashboardService

    def get_studenten(self) -> list[Student]:
        return self._student_rep.lade_alle()

    def get_student(self, matrikelnummer: str):
        try:
            student = self._student_rep.lade_student(matrikelnummer)
        except TypeError:
            return None, "Student wurde nicht gefunden."
        return student, None

    def lade_dashboard_daten(self, matrikelnummer: str):
        try:
            student = self._student_rep.lade_student(matrikelnummer)
            student.studiengang = self._studiengang_rep.lade_studiengang_von_student(student.matrikelnummer)
            student.pruefungsleistungen = self._pruefungsleistung_rep.lade_pruefungsleistung_von_student(student)

            student.studiengang.semester = self._semester_rep.lade_semester_von_studiengang(student.studiengang)
            for semester in student.studiengang.semester:
                semester.module = self._modul_rep.lade_module_von_semester(semester)

            studienfortschritt = self._dashboard_service.berechne_studienfortschritt(student)
            aktueller_notendurchschnitt = student.aktuellerNotendurchschnitt
            erforderliche_note, durchschnitt_neu = self._dashboard_service.berechne_erforderliche_note(student)

            studiendauer_fortschritt = self._dashboard_service.berechne_studiendauer_fortschritt(student)
            verbleibende_dauer = self._dashboard_service.berechne_verbleibende_dauer(student)
            verfuegbare_dauer_pro_modul = self._dashboard_service.berechne_verfuegbare_dauer_pro_modul(student)

            semester_dtos = []
            for semester in student.studiengang.semester:
                notendurchschnitt = self._dashboard_service.berechne_semester_notendurchschnitt(semester, student)
                status = self._dashboard_service.berechne_semester_status(semester, student)

                modul_dtos = []
                for modul in semester.module:
                    pruefungsleistung = self._dashboard_service.get_pruefungsleistung(student, modul)
                    note = None
                    modul_status = Status.OFFEN

                    if pruefungsleistung:
                        note = pruefungsleistung.note
                        modul_status = pruefungsleistung.status

                    modul_dto = ModulDTO(modul=modul, note=note, status=modul_status)
                    modul_dtos.append(modul_dto)

                semester_dto = SemesterDTO(semester=semester, notendurchschnitt=notendurchschnitt, status=status, module=modul_dtos)
                semester_dtos.append(semester_dto)
        except TypeError:
            return None, "Kein Modul gefunden. Bitte überprüfe die Eingaben in Studenten- und Studiengang Verwalten"
        except Exception as e:
            return None, f"Ein unerwarteter Fehler ist aufgetreten.\n{e}"

        return DashboardDTO(
            student=student,
            studiengang=student.studiengang,
            studienfortschritt=studienfortschritt,
            aktueller_notendurchschnitt=aktueller_notendurchschnitt,
            erforderliche_note=erforderliche_note,
            notendurchschnitt_bei_erfolgreicher_note=durchschnitt_neu,
            studiendauer_fortschritt=studiendauer_fortschritt,
            verbleibende_dauer=verbleibende_dauer,
            verfuegbare_dauer_pro_modul=verfuegbare_dauer_pro_modul,
            semester=semester_dtos,
        ), None