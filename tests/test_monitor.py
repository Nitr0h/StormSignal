from stw_presence.fortnite.monitor import (
    FortniteProcessEvent,
    FortniteProcessMonitor,
    get_process_event,
)


def test_fortnite_started() -> None:
    event = get_process_event(was_running=False, is_running=True)

    assert event == FortniteProcessEvent.STARTED


def test_fortnite_stopped() -> None:
    event = get_process_event(was_running=True, is_running=False)

    assert event == FortniteProcessEvent.STOPPED


def test_fortnite_still_running() -> None:
    event = get_process_event(was_running=True, is_running=True)

    assert event is None


def test_fortnite_still_closed() -> None:
    event = get_process_event(was_running=False, is_running=False)

    assert event is None


def test_process_monitor_tracks_changers() -> None:
    states = iter([False, True, True, False])

    def fake_is_running() -> bool:
        return next(states)

    monitor = FortniteProcessMonitor(fake_is_running)

    assert monitor.poll() is None
    assert monitor.poll() == FortniteProcessEvent.STARTED
    assert monitor.poll() is None
    assert monitor.poll() == FortniteProcessEvent.STOPPED


def test_process_monitor_detects_already_running() -> None:
    def fake_is_running() -> bool:
        return True

    monitor = FortniteProcessMonitor(fake_is_running)

    assert monitor.poll() == FortniteProcessEvent.STARTED


def test_process_monitor_can_start_already_running() -> None:
    def fake_is_running() -> bool:
        return True

    monitor = FortniteProcessMonitor(
        fake_is_running,
        initially_running=True,
    )

    assert monitor.poll() is None
