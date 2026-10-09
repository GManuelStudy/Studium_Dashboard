from dataclasses import dataclass
from Model.modul import Modul
from Model.status import Status

@dataclass
class PruefungsleistungDTO:
    """ Ergänzt Prüfungsleistung für Modul.
    Fehlende Prüfung wird mit note=None und Status.OFFEN angezeigt.
    """
    modul: Modul
    note: float | None
    status: Status