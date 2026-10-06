from stw_presence.config import AppConfig
from stw_presence.models import MissionPhase, STWState


def build_state_text(state: STWState, config: AppConfig) -> str:
    parts: list[str] = []

    if state.mission:
        power_level: str = f"PL {state.mission.power_level}"
        parts.append(power_level)

    if config.presence.show_commander is True and state.commander is not None:
        parts.append(state.commander.name)

    if config.presence.show_streak is True:
        streak: str = f"On a {state.current_streak} mission streak!"
        parts.append(streak)

    return " • ".join(parts)


def build_details(state: STWState) -> str:
    if state.phase == MissionPhase.OFFLINE:
        return "Fortnite Offline"
    if state.phase == MissionPhase.HOMEBASE:
        return "Hangin' out in Homebase"
    if state.phase == MissionPhase.PREPARING:
        if state.mission is None:
            return "Preparing for a mission"

        return f"Preparing to {state.mission.name}"
    if state.phase == MissionPhase.LOADING:
        return "Heading into a mission"
    if state.phase == MissionPhase.IN_MISSION:
        return "Saving the World"
    if state.phase == MissionPhase.COMPLETED:
        return "Returning to Homebase"

    return "Save The World"
