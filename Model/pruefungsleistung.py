from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from Model.status import Status

if TYPE_CHECKING:
    from Model.modul import Modul
    from Model.student import Student

@dataclass
class Pruefungsleistung:
    student : Student
    modul : Modul
    note : float| None
    status : Status = Status.OFFEN
