from Model.modul import Modul
from Model.studiengang import Studiengang
from Model.semester import Semester
from Model.status import Status
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.semester_repository_abstract import SemesterRepositoryAbstract
from Views.studiengangView import Studiengang_Verwalten


class StudiengangController:
    def __init__(self, studiengang_repository: StudiengangRepositoryAbstract, modul_repositoy: ModulRepositoryAbstract, semester_repository: SemesterRepositoryAbstract) -> None:
        self._studiengang_rep = studiengang_repository
        self._modul_rep = modul_repositoy
        self._semester_rep = semester_repository

    def get_studiengaenge(self) -> list[Studiengang]:
        studiengaenge_temp = self._studiengang_rep.lade_alle()
        studiengaenge = []

        for studiengang in studiengaenge_temp:
            studiengang.semester = self._semester_rep.lade_semester_von_studiengang(studiengang)
            for semester in studiengang.semester:
                semester.module = self._modul_rep.lade_module_von_semester(semester)
            studiengaenge.append(studiengang)

        return studiengaenge

    def get_studiengang(self, bezeichnung: str) -> Studiengang:
        studiengang = Studiengang(studiengang=bezeichnung)
        return self._studiengang_rep.lade_studiengang(studiengang)

    def add_studiengang(self, bezeichnung: str):
        bezeichnung = bezeichnung.strip()
        if not bezeichnung:
            return None, "Die Bezeichnung darf nicht leer sein."

        studiengang = Studiengang(studiengang=bezeichnung)
        #
        # if self._studiengang_rep.lade_studiengang(studiengang) is not None:
        #     return None, "Der Studiengang existiert bereits."
        try:
            studiengang_neu = self._studiengang_rep.speichern(studiengang)
            return studiengang_neu, None
        except ValueError:
            return None, "Der Studiengang existiert bereits."



    def update_studiengang(self, studiengang: Studiengang, bezeichnung_neu: str):
        # studiengang_s = studiengang_rep.lade_studiengang(studiengang)
        # if studiengang_s is not None and studiengang_s.id != id:
        #     return

        self._studiengang_rep.aktualisieren(studiengang, bezeichnung_neu)
        studiengang.studiengang = bezeichnung_neu
        # self.show_page(StudiengangForm, self, studiengang=studiengang)

    def del_studiengang(self, studiengang_bez: str):
        self._studiengang_rep.loeschen(Studiengang(studiengang_bez))

    def get_module(self, studiengang: Studiengang) -> list[Modul]:
        module = self._modul_rep.lade_module_von_studiengang(studiengang)
        return module

    def add_module(self, modulname: str, modulcode: str, ects: int, semester_num: int, studiengang: Studiengang):
        if not studiengang:
            return None, "Studiengang ist nicht vorhanden."

        if modulname == "" or modulcode == "" or ects == "" or semester_num == "":
            return None, "Alle Modul-Eingabefelder müssen befüllt sein."
        semester_list = self._semester_rep.lade_semester_von_studiengang(studiengang)

        semester = next((item for item in semester_list if item.semester == int(semester_num)), None)
        if semester is None:
            semester = Semester(semester_num, studiengang)
            self._semester_rep.speichern(semester)
            # semester = next(item for item in semester_list if item.semester == semester)
            # studiengang.semester.append(semester)

        modul = Modul(modulcode, modulname, ects, semester)
        try:
            self._modul_rep.speichern(modul)
        except ValueError:
            return None, f"Ein Modul mit dem Modulcode \"{modulcode}\" existiert bereits."
        semester.module.append(modul)
        return modul, None

    def del_modul(self, modulcode: str):
        modul = self._modul_rep.lade_modul(modulcode)
        semester = modul.semester
        self._modul_rep.loeschen(modulcode)

        module = self._modul_rep.lade_module_von_semester(modul.semester)
        if not module:
            self._semester_rep.loeschen(semester)
