from enum import Enum, auto


class FortniteLogEvent(Enum):
    STW_ACTIVATED = auto()
    STW_DEACTIVATED = auto()

    MISSION_LOADING = auto()
    MISSION_STARTED = auto()

    RETURNING_TO_HOMEBASE = auto()
    HOMEBASE_READY = auto()


def parse_log_line(line: str) -> FortniteLogEvent | None:
    if (
        "Game feature 'SaveTheWorld' transitioned successfully." in line
        and "Ending state: Active [Active, Active]" in line
    ):
        return FortniteLogEvent.STW_ACTIVATED

    if (
        "Game feature 'SaveTheWorld' transitioned successfully." in line
        and "Ending state: Registered [Terminal, Registered]" in line
    ):
        return FortniteLogEvent.STW_DEACTIVATED

    if "LoadMap(/STW_Zones/Maps/Zones/" in line:
        return FortniteLogEvent.MISSION_LOADING

    if "Snapshot: Start of Match (FortGameStatePvE" in line:
        return FortniteLogEvent.MISSION_STARTED

    if "Old Location: {InGame}" in line and "New Location: {ConnectingToLobby}" in line:
        return FortniteLogEvent.RETURNING_TO_HOMEBASE

    if "Snapshot: Start of Match (FortGameStateHestiaBeauty" in line:
        return FortniteLogEvent.HOMEBASE_READY

    return None


def parse_mission_id(line: str) -> str | None:
    if "STW:Mission [" not in line:
        return None 

    mission_id = line.split("[", 1)[1][:-1]

    return mission_id
