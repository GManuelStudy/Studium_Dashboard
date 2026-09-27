from Repository.abstract_repository.student_repository_abstract import StudentRepositoryAbstract as student_rep

class StudentController:
    def __init__(self, repository: student_rep) -> None:
        self._repository = repository