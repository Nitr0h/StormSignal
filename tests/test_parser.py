from stw_presence.fortnite.parser import (
    FortniteLogEvent,
    parse_log_line,
    parse_mission_id,
)


def test_parses_stw_activated() -> None:
    line = (
        "Game feature 'SaveTheWorld' transitioned successfully. "
        "Ending state: Active [Active, Active]"
    )

    assert parse_log_line(line) == FortniteLogEvent.STW_ACTIVATED


def test_parses_stw_deactivated() -> None:
    line = (
        "Game feature 'SaveTheWorld' transitioned successfully. "
        "Ending state: Registered [Terminal, Registered]"
    )

    assert parse_log_line(line) == FortniteLogEvent.STW_DEACTIVATED


def test_parses_mission_loading() -> None:
    line = "LoadMap(/STW_Zones/Maps/Zones/Zone_Temperate_Forest)"

    assert parse_log_line(line) == FortniteLogEvent.MISSION_LOADING


def test_parses_mission_started() -> None:
    line = "Snapshot: Start of Match (FortGameStatePvE...)"

    assert parse_log_line(line) == FortniteLogEvent.MISSION_STARTED


def test_parses_returning_to_homebase() -> None:
    line = "Old Location: {InGame} / New Location: {ConnectingToLobby}"

    assert parse_log_line(line) == FortniteLogEvent.RETURNING_TO_HOMEBASE


def test_parses_homebase_ready() -> None:
    line = "Snapshot: Start of Match (FortGameStateHestiaBeauty...)"

    assert parse_log_line(line) == FortniteLogEvent.HOMEBASE_READY


def test_ignores_unrelated_line() -> None:
    line = "LogFortAnimation: completely unrelated"

    assert parse_log_line(line) is None


def test_parse_mission_id() -> None:
    line = "STW:Mission [3704a5b0-ca32-4e56-b284-72f39f15a0c7]"

    assert parse_mission_id(line) == "3704a5b0-ca32-4e56-b284-72f39f15a0c7"


def test_parse_mission_id_ignores_unrelated_line() -> None:
    line = "LogFort: completely unrelated"

    assert parse_mission_id(line) is None
