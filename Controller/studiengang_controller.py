from Model.studiengang import Studiengang
from Repository.abstract_repository.studiengang_repository_abstract import StudiengangRepositoryAbstract as studiengang_rep

class StudiengangController:
    def __init__(self, repository: studiengang_rep) -> None:
        self._repository = repository

    def get_studiengaenge(self) -> list[Studiengang]:
        return self._repository.lade_alle()