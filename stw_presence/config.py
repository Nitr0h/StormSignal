import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PresenceSettings:
    show_commander: bool
    show_streak: bool
    show_party_size: bool
    use_flavor_text: bool


@dataclass
class TrackingSettings:
    track_mission_history: bool


@dataclass
class DiscordSettings:
    application_id: str


@dataclass
class AppConfig:
    presence: PresenceSettings
    tracking: TrackingSettings
    discord: DiscordSettings


def load_config(path: Path) -> AppConfig:
    with path.open("rb") as file:
        data = tomllib.load(file)

    presence_data = data["presence"]
    tracking_data = data["tracking"]
    discord_data = data["discord"]

    presence = PresenceSettings(
        show_commander=presence_data["show_commander"],
        show_streak=presence_data["show_streak"],
        show_party_size=presence_data["show_party_size"],
        use_flavor_text=presence_data["use_flavor_text"],
    )

    tracking = TrackingSettings(
        track_mission_history=tracking_data["track_mission_history"]
    )

    discord = DiscordSettings(application_id=discord_data["application_id"])

    return AppConfig(presence=presence, tracking=tracking, discord=discord)
