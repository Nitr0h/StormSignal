import json
from pathlib import Path

from stw_presence.models import Mission

MISSION_NAMES: dict
mission_name_path = Path("data/MissionGen.json")
with mission_name_path.open("r", encoding="utf-8") as names:
    raw_mission_data = json.load(names)

MISSION_NAMES = {
    entry["Name"]: entry["DisplayName"] for entry in raw_mission_data.values()
}

POWER_LEVELS = {
    "Theater_Start_Zone1": 1,
    "Theater_Start_Zone2": 3,
    "Theater_Start_Zone3": 5,
    "Theater_Start_Zone4": 9,
    "Theater_Start_Zone5": 15,
    "Theater_Normal_Zone1": 19,
    "Theater_Normal_Zone2": 23,
    "Theater_Normal_Zone3": 28,
    "Theater_Normal_Zone4": 34,
    "Theater_Normal_Zone5": 40,
    "Theater_Hard_Zone1": 46,
    "Theater_Hard_Zone2": 52,
    "Theater_Hard_Zone3": 58,
    "Theater_Hard_Zone4": 64,
    "Theater_Hard_Zone5": 70,
    "Theater_Nightmare_Zone1": 76,
    "Theater_Nightmare_Zone2": 82,
    "Theater_Nightmare_Zone3": 88,
    "Theater_Nightmare_Zone4": 94,
    "Theater_Nightmare_Zone5": 100,
}


def find_mission_by_guid(
    mission_groups: list[dict],
    mission_id: str,
) -> tuple[dict, dict] | None:
    for mission_group in mission_groups:
        for mission in mission_group["availableMissions"]:
            if mission["missionGuid"] == mission_id:
                return mission, mission_group

    return None


def find_theater_by_id(
    theaters: list[dict],
    theater_id: str,
) -> dict | None:
    for theater in theaters:
        if theater["uniqueId"] == theater_id:
            return theater

    return None


def get_power_level(row_name: str) -> int | None:
    if POWER_LEVELS.get(row_name) is not None:
        return POWER_LEVELS.get(row_name)
    else:
        return None


def get_mission_name(generator_path: str) -> str | None:
    generator_name = generator_path.rsplit(".", 1)[-1]

    if generator_name is not None:
        return MISSION_NAMES.get(generator_name)
    else:
        return "Unknown"


def resolve_mission(world_data: dict, mission_id: str) -> Mission | None:
    result = find_mission_by_guid(world_data["missions"], mission_id)

    if result is None:
        raise RuntimeError(f"Mission not found: {mission_id}")

    if result is None:
        return None

    mission, mission_group = result

    theater = find_theater_by_id(
        world_data["theaters"],
        mission_group["theaterId"],
    )

    if theater is None:
        return None

    row_name = mission["missionDifficultyInfo"]["rowName"]
    power_level = get_power_level(row_name)
    mission_name = get_mission_name(mission["missionGenerator"])

    # print("Mission:", mission_name)
    # print("Mission GUID:", mission["missionGuid"])
    # print("Theater:", theater["displayName"]["en"])
    # print("Power Level:", power_level)
    # print("Tile:", mission["tileIndex"])
    # print("Difficulty row:", row_name)
    # print("Mission generator:", generator_name)

    return Mission(mission_name, power_level, theater["displayName"]["en"])
