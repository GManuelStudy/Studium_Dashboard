from enum import StrEnum

class Status(StrEnum):
    """Wird für Pruefungsleistungen verwendet."""
    ABGESCHLOSSEN = "Abgeschlossen"
    OFFEN = "Offen"
    NICHT_BESTANDEN = "Nicht bestanden"