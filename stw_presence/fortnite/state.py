from stw_presence.fortnite.parser import FortniteLogEvent, parse_log_line
from stw_presence.models import MissionPhase


def reconstruct_phase(lines: list[str]) -> MissionPhase:
    current_phase = MissionPhase.UNKNOWN

    for line in lines:
        event = parse_log_line(line)

        if event is None:
            continue

        phase = phase_from_event(event)

        if phase is None:
            continue

        current_phase = phase

    return current_phase


def phase_from_event(
    event: FortniteLogEvent,
) -> MissionPhase | None:
    if (
        event == FortniteLogEvent.STW_ACTIVATED
        or event == FortniteLogEvent.MISSION_LOADING
        or event == FortniteLogEvent.RETURNING_TO_HOMEBASE
    ):
        return MissionPhase.LOADING
    elif event == FortniteLogEvent.MISSION_STARTED:
        return MissionPhase.IN_MISSION
    elif event == FortniteLogEvent.HOMEBASE_READY:
        return MissionPhase.HOMEBASE
    elif event == FortniteLogEvent.STW_DEACTIVATED:
        return MissionPhase.OFFLINE

    return None
