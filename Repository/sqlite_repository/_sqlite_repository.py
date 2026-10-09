from contextlib import closing
import sqlite3
from Repository.database import Database

class SQLiteRepository:
    """Gemeinsames Repository zum Verwalten der Transaktionen innerhalb der Datenbank.
    Fehlende Datensätze erzeugen TypeError,
    Doppelte Schlüssel und verletzte Integritätsbedingungen erzeugen ValueError.
    """
    def __init__(self, database: Database):
        """Initalisiert benötigte Abhängigkeit zur Datenbank."""
        self.database = database

    def _lade_eine_zeile(self, sql, parameter=()):
        """Lade eine Zeile einer SQLite-Abfrage.
        Ohne Treffer gilt TypeError. Integritätsfehler erzeugen ValueError.
        """
        with closing(self.database.get_connection()) as connection:
            row = connection.execute(sql, parameter).fetchone()
        return row

    def _lade_zeilen(self, sql, parameter=()):
        """Liefert alle Treffer einer SQLite-Abfrage als Liste."""
        with closing(self.database.get_connection()) as connection:
            return connection.execute(sql, parameter).fetchall()

    def _schreiben(self, sql, parameter) -> int | None:
        """Führt einen INSERT, UPDATE oder DELETE-Befehl aus und liefert cursor.lastrowid.
        Bei fehlendem Treffer gilt TypeError. Integritätsfehler erzeugen ValueError.
        """
        with closing(self.database.get_connection()) as connection:
            try:
                with connection:
                    cursor = connection.execute(sql, parameter)
                    if cursor.rowcount == 0:
                        raise TypeError("Der zu ändernde Datensatz wurde nicht gefunden.")
                    return cursor.lastrowid
            except sqlite3.IntegrityError as error:
                raise ValueError(
                    "Datenbankbedingung verletzt: doppelter Schlüssel, fehlender "
                    "Pflichtwert oder unzulässige Verknüpfung. " + str(error)
                ) from error
