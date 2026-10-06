from dataclasses import dataclass
from enum import Enum, auto


class MissionPhase(Enum):
    OFFLINE = auto()
    HOMEBASE = auto()
    PREPARING = auto()
    LOADING = auto()
    IN_MISSION = auto()
    COMPLETED = auto()
    UNKNOWN = auto()


@dataclass
class Hero:
    name: str


@dataclass
class Mission:
    name: str
    power_level: int
    theater: str


@dataclass
class STWState:
    phase: MissionPhase
    commander: Hero | None
    mission: Mission | None
    party_size: int
    current_streak: int
