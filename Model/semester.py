from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Model.studiengang import Studiengang
    from Model.modul import Modul

@dataclass
class Semester:
    semester : int
    studiengang : Studiengang
    module : list[Modul] = field(default_factory=list)
