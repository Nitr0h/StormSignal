from stw_presence.fortnite.mission import get_power_level, resolve_mission


def test_get_power_level() -> None:
    assert get_power_level("Theater_Start_Zone1") == 1
    assert get_power_level("Theater_Nightmare_Zone5") == 100
    assert get_power_level("Something_Unknown") is None


def test_resolve_mission_returns_metadata() -> None:
    WORLD_DATA = {
        "missions": [
            {
                "theaterId": "stonewood-id",
                "availableMissions": [
                    {
                        "missionGuid": "test-guid",
                        "missionGenerator": (
                            "/SaveTheWorld/World/MissionGens/"
                            "MissionGen_T1_LT_LtB.MissionGen_T1_LT_LtB_C"
                        ),
                        "missionDifficultyInfo": {"rowName": "Theater_Start_Zone2"},
                        "tileIndex": 3,
                    }
                ],
            }
        ],
        "theaters": [
            {
                "uniqueId": "stonewood-id",
                "displayName": {"en": "Stonewood"},
            }
        ],
    }

    mission = resolve_mission(WORLD_DATA, "test-guid")

    assert mission is not None
    assert mission.name == "Ride The Lightning"
    assert mission.power_level == 3
    assert mission.theater == "Stonewood"
