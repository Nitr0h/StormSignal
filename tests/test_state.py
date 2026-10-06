from stw_presence.fortnite.parser import FortniteLogEvent, parse_log_line
from stw_presence.fortnite.state import phase_from_event
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


def test_state_loading_mapping() -> None:
    loading_events = (
        FortniteLogEvent.STW_ACTIVATED,
        FortniteLogEvent.MISSION_LOADING,
        FortniteLogEvent.RETURNING_TO_HOMEBASE,
    )

    for event in loading_events:
        assert phase_from_event(event) == MissionPhase.LOADING


def test_state_change_mapping() -> None:
    assert phase_from_event(FortniteLogEvent.MISSION_STARTED) == MissionPhase.IN_MISSION
    assert phase_from_event(FortniteLogEvent.HOMEBASE_READY) == MissionPhase.HOMEBASE
    assert phase_from_event(FortniteLogEvent.STW_DEACTIVATED) == MissionPhase.OFFLINE


def test_reconstruction() -> None:
    assert reconstruct_phase([]) == MissionPhase.UNKNOWN
    assert (
        reconstruct_phase(["Snapshot: Start of Match (FortGameStateHestiaBeauty"])
        == MissionPhase.HOMEBASE
    )


def test_reconstruction_uses_latest_meaningful_event() -> None:
    lines = [
        "completely unrelated line",
        "Snapshot: Start of Match (FortGameStateHestiaBeauty",
        "another useless log message",
        "LoadMap(/STW_Zones/Maps/Zones/Zone_Temperate_Forest)",
        "Snapshot: Start of Match (FortGameStatePvE",
    ]

    assert reconstruct_phase(lines) == MissionPhase.IN_MISSION
