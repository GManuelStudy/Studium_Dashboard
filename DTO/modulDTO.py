from dataclasses import dataclass
from Model.modul import Modul
from Model.status import Status


@dataclass
class ModulDTO:
    modul: Modul
    note: float | None
    status: Status