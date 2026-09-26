import sqlite3

class Database:
    def __init__(self, db_pfad: str = "Repository/studium_dashboard.db") -> None:
        self._db_pfad = db_pfad

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_pfad)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_database(self) -> None:
        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.executescript(f"""
            CREATE TABLE IF NOT EXISTS Studiengang (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                bezeichnung     TEXT    NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Student (
                id                          INTEGER PRIMARY KEY AUTOINCREMENT,
                vorname                     TEXT    NOT NULL,
                nachname                    TEXT    NOT NULL,
                matrikelnummer              TEXT    NOT NULL UNIQUE,
                studiengang_id              INTEGER NOT NULL,
                zielnotendurchschnitt       REAL,
                aktuellerNotendurchschnitt  REAL,
                aktuelleECTS                INTEGER,
                beginndatum                 DATE,
                zielabschlussdatum          DATE,
                FOREIGN KEY (studiengang_id) REFERENCES Studiengang (id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Semester (
                id                              INTEGER PRIMARY KEY AUTOINCREMENT,
                semester                        INTEGER NOT NULL,
                status                          TEXT    NOT NULL,
                studiengang_id                  INTEGER NOT NULL,
                UNIQUE (semester, studiengang_id),
                FOREIGN KEY (studiengang_id)    REFERENCES Studiengang (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Modul (
                id           INTEGER    PRIMARY KEY AUTOINCREMENT,
                modulname    TEXT       NOT NULL,
                modulcode    TEXT       NOT NULL UNIQUE,
                ects         INTEGER    NOT NULL,
                semester_id  INTEGER    NOT NULL,
                FOREIGN KEY (semester_id) REFERENCES Semester (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS Pruefungsleistung (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id  INTEGER NOT NULL,
                modul_id    INTEGER NOT NULL,
                note        REAL,
                status      TEXT    NOT NULL,
                UNIQUE (student_id, modul_id),
                FOREIGN KEY (student_id) REFERENCES Student (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (modul_id) REFERENCES Modul (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_student_studiengang ON Student (studiengang_id);
            CREATE INDEX IF NOT EXISTS idx_semester_studiengang ON Semester (studiengang_id);
            CREATE INDEX IF NOT EXISTS idx_modul_semester ON Modul (semester_id);
            CREATE INDEX IF NOT EXISTS idx_pl_student ON Pruefungsleistung (student_id);
            CREATE INDEX IF NOT EXISTS idx_pl_modul ON Pruefungsleistung (modul_id);
            """)

        connection.commit()
        connection.close()