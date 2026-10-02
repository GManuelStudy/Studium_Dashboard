from DTO.dashboardDTO import DashboardDTO
from Repository.abstract_repository.modul_repository_abstract import ModulRepositoryAbstract
from Repository.abstract_repository.pruefungsleistung_repository_abstract import PruefungsleistungRepositoryAbstract
from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract
from Repository.abstract_repository.semester_repository_abstract import SemesterRepositoryAbstract
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract

class DashboardController:
    def __init__(self, student_repository: StudentRepositoryAbstract, modul_repository: ModulRepositoryAbstract, pruefungsleistung_repository: PruefungsleistungRepositoryAbstract, studiengang_repository: StudiengangRepositoryAbstract, semester_repository: SemesterRepositoryAbstract) -> None:
        self._student_rep = student_repository
        self._modul_rep = modul_repository
        self._pruefungsleistung_rep = pruefungsleistung_repository
        self._studiengang_rep = studiengang_repository
        self._semester_rep = semester_repository

    def get_studenten(self):
        return self._student_rep.lade_alle()

    def lade_dashboard_daten(self) -> DashboardDTO:
        pass