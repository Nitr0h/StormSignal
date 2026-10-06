import time
from pathlib import Path

from stw_presence.config import load_config
from stw_presence.discord.rpc import DiscordRPC
from stw_presence.fortnite.logs import FortniteLogTailer, get_fortnite_log_path
from stw_presence.fortnite.monitor import FortniteProcessEvent, FortniteProcessMonitor
from stw_presence.fortnite.parser import parse_log_line
from stw_presence.fortnite.process import is_fortnite_running
from stw_presence.fortnite.state import phase_from_event, reconstruct_phase
from stw_presence.models import Hero, Mission, MissionPhase, STWState
from stw_presence.presence import build_details, build_state_text


def main() -> None:
    config_path = Path("configs/config.toml")
    config = load_config(config_path)

    def update_presence() -> None:
        details = build_details(state)
        state_text = build_state_text(state, config)

        discord.update(
            details=details,
            state_text=state_text,
        )

    def set_phase(new_phase: MissionPhase) -> None:
        if state.phase == new_phase:
            return

        state.phase = new_phase
        update_presence()

        print(f"Phase changed to: {state.phase}")

    def print_debug_line(line: str) -> None:
        max_length = 500

        if len(line) > max_length:
            print(f"{line[:max_length]}... [truncated {len(line) - max_length} chars]")
        else:
            print(line)

    state = STWState(
        phase=MissionPhase.UNKNOWN,
        commander=Hero(name="B.A.S.E Kyle"),
        mission=Mission(
            name="Ride The Lightning",
            power_level=160,
            theater="Twine Peaks",
        ),
        party_size=3,
        current_streak=7,
    )

    fortnite_running = is_fortnite_running()

    monitor = FortniteProcessMonitor(
        is_fortnite_running,
        initially_running=fortnite_running,
    )
    log_tailer = FortniteLogTailer(get_fortnite_log_path())
    discord = DiscordRPC(config.discord.application_id)
    discord.connect()

    if fortnite_running:
        recent_lines = log_tailer.read_recent_lines(250_000)
        reconstructed_phase = reconstruct_phase(recent_lines)

        set_phase(reconstructed_phase)
        log_tailer.start_at_end()

    try:
        while True:
            event = monitor.poll()

            if event is not None:
                print(f"Process event: {event}")

            if event == FortniteProcessEvent.STARTED:
                log_tailer.start_at_end()
                state.phase = MissionPhase.UNKNOWN

            elif event == FortniteProcessEvent.STOPPED:
                if state.phase != MissionPhase.OFFLINE:
                    state.phase = MissionPhase.OFFLINE
                    discord.clear()
                    print(f"Phase changed to: {state.phase}")

            if is_fortnite_running():
                for line in log_tailer.poll():
                    log_event = parse_log_line(line)

                    if log_event is None:
                        continue

                    phase = phase_from_event(log_event)

                    if phase is None:
                        continue

                    if phase == MissionPhase.OFFLINE:
                        if state.phase != MissionPhase.OFFLINE:
                            state.phase = MissionPhase.OFFLINE
                            discord.clear()
                            print(f"Phase changed to: {state.phase}")
                    else:
                        set_phase(phase)

            time.sleep(2)
    finally:
        discord.clear()


if __name__ == "__main__":
    main()
