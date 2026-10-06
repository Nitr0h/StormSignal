from stw_presence.fortnite.process import is_fortnite_running


class FakeProcess:
    def __init__(self, name: str) -> None:
        self.info = {"name": name}


def test_fortnite_running(monkeypatch) -> None:
    processes = [
        FakeProcess("Discord.exe"),
        FakeProcess("chrome.exe"),
        FakeProcess("FortniteClient-Win64-Shipping.exe"),
    ]

    monkeypatch.setattr(
        "stw_presence.fortnite.process.psutil.process_iter",
        lambda attrs: processes,
    )

    result = is_fortnite_running()

    assert result is True


def test_fortnite_not_running(monkeypatch) -> None:
    processes = [
        FakeProcess("Discord.exe"),
        FakeProcess("chrome.exe"),
        FakeProcess("explorer.exe"),
    ]

    monkeypatch.setattr(
        "stw_presence.fortnite.process.psutil.process_iter",
        lambda attrs: processes,
    )

    result = is_fortnite_running()

    assert result is False
