from Controller.dashboard_controller import DashboardController
from Controller.home_controller import HomeController
from Controller.student_controller import StudentController
from Controller.studiengang_controller import StudiengangController
from Repository.sqlite_repository.sqlite_modul_repository import SQLiteModulRepository
from Repository.sqlite_repository.sqlite_pruefungsleistung_repository import SQLitePruefungsleistungRepository
from Repository.sqlite_repository.sqlite_semester_repository import SQLiteSemesterRepository
from Repository.sqlite_repository.sqlite_student_repository import SQLiteStudentRepository
from Repository.sqlite_repository.sqlite_studiengang_repository import SQLiteStudiengangRepository
from Repository.database import Database
from Views.mainWindow import App

class DashboardApp:
    def __init__(self) -> None:
        self._db = Database()
        self._app = App("Studium Dashboard", (1200, 800))

        self._studiengang_rep = SQLiteStudiengangRepository(self._db)
        self._semester_rep = SQLiteSemesterRepository(self._db, self._studiengang_rep)
        self._modul_rep = SQLiteModulRepository(self._db, self._studiengang_rep)
        self._semester_rep.modul_repository = self._modul_rep
        self._modul_rep.semester_repository = self._semester_rep
        self._student_rep = SQLiteStudentRepository(self._db, self._studiengang_rep)
        self._pruefungsleistung_rep = SQLitePruefungsleistungRepository(self._db)
        self._pruefungsleistung_rep.student_repository = self._student_rep
        self._pruefungsleistung_rep.modul_repository = self._modul_rep

        self._studiengang_controller = StudiengangController(self._studiengang_rep, self._modul_rep, self._semester_rep)
        self._student_controller = StudentController(self._student_rep, self._modul_rep, self._pruefungsleistung_rep)
        self._dashboard_controller = DashboardController(self._student_rep, self._modul_rep, self._pruefungsleistung_rep, self._studiengang_rep, self._semester_rep)
        self._dashboard_controller = HomeController(self._app, self._studiengang_controller, self._student_controller, self._dashboard_controller)


    def start(self) -> None:
        self._db.initialize_database()
        self._app.mainloop()