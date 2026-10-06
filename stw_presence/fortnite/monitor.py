from collections.abc import Callable
from enum import Enum, auto


class FortniteProcessEvent(Enum):
    STARTED = auto()
    STOPPED = auto()


class FortniteProcessMonitor:
    def __init__(
        self,
        is_running: Callable[[], bool],
        initially_running: bool = False,
    ) -> None:
        self._is_running = is_running
        self._was_running = initially_running

    def poll(self) -> FortniteProcessEvent | None:
        current_state: bool = self._is_running()
        event = get_process_event(
            was_running=self._was_running, is_running=current_state
        )

        self._was_running = current_state

        return event


def get_process_event(
    was_running: bool, is_running: bool
) -> FortniteProcessEvent | None:
    if was_running is False and is_running is True:
        return FortniteProcessEvent.STARTED

    if was_running is True and is_running is False:
        return FortniteProcessEvent.STOPPED

    return None
