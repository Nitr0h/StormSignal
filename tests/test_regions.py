from ..scripts.inspect_world_info import find_region_for_tile, get_power_level


def test_find_region_for_tile() -> None:
    regions = [
        {"uniqueId": "Region_A", "tileIndices": [1, 2, 3]},
        {"uniqueId": "Region_B", "tileIndices": [10, 28, 30]},
    ]

    region = find_region_for_tile(regions, 28)

    assert region is not None
    assert region["uniqueId"] == "Region_B"


def test_find_region_for_tile_returns_none_when_missing() -> None:
    regions = [
        {"uniqueId": "Region_A", "tileIndices": [1, 2, 3]},
    ]

    assert find_region_for_tile(regions, 99) is None


def test_get_power_level() -> None:
    assert get_power_level("Theater_Start_Zone1") == 1
    assert get_power_level("Theater_Nightmare_Zone5") == 100
    assert get_power_level("Something_Unknown") is None
