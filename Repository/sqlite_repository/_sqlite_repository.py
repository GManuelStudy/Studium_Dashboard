"""Gemeinsame SQL-Ausführung; technische IDs bleiben in der Repository-Schicht."""

from contextlib import closing
import sqlite3

from Repository.database import Database


class SQLiteRepository:
    def __init__(self, database: Database):
        self.database = database

    def _lade_eine_zeile(self, sql, parameter=()):
        with closing(self.database.get_connection()) as connection:
            row = connection.execute(sql, parameter).fetchone()
        if row is None:
            raise ValueError("Der gesuchte Datensatz wurde nicht gefunden.")
        return row

    def _lade_zeilen(self, sql, parameter=()):
        with closing(self.database.get_connection()) as connection:
            return connection.execute(sql, parameter).fetchall()

    def _schreiben(self, sql, parameter, *, muss_existieren=False) -> int | None:
        with closing(self.database.get_connection()) as connection:
            try:
                with connection:
                    cursor = connection.execute(sql, parameter)
                    if muss_existieren and cursor.rowcount == 0:
                        raise ValueError("Der zu ändernde Datensatz wurde nicht gefunden.")
                    return cursor.lastrowid
            except sqlite3.IntegrityError as error:
                raise ValueError(
                    "Datenbankbedingung verletzt: doppelter Schlüssel, fehlender "
                    "Pflichtwert oder unzulässige Verknüpfung. " + str(error)
                ) from error
