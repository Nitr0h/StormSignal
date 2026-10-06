from pathlib import Path

from stw_presence.fortnite.logs import FortniteLogTailer


def test_log_tailer_reads_only_new_lines(tmp_path: Path) -> None:
    log_path = tmp_path / "FortniteGame.log"

    log_path.write_text(
        "old line 1\nold line 2\n",
        encoding="utf-8",
    )

    tailer = FortniteLogTailer(log_path)
    tailer.start_at_end()

    with log_path.open("a", encoding="utf-8") as file:
        file.write("new line 1\n")
        file.write("new line 2\n")

    lines = tailer.poll()

    assert lines == [
        "new line 1",
        "new line 2",
    ]

    assert tailer.poll() == []


def test_log_tailer_handles_truncated_file(tmp_path: Path) -> None:
    log_path = tmp_path / "FortniteGame.log"

    log_path.write_text(
        "old line 1\nold line 2\nold line 3\n",
        encoding="utf-8",
    )

    tailer = FortniteLogTailer(log_path)
    tailer.start_at_end()

    # Simulate Fortnite replacing/truncating its log.
    log_path.write_text(
        "new session line 1\n",
        encoding="utf-8",
    )

    lines = tailer.poll()

    assert lines == ["new session line 1"]


def test_log_smaller_than_max(tmp_path: Path) -> None:
    log_path = tmp_path / "FortniteGame.log"

    line = "A very small log line"

    log_path.write_text(
        f"{line}\n",
        encoding="utf-8",
    )

    tailer = FortniteLogTailer(log_path)

    assert tailer.read_recent_lines(10_000) == [line]


def test_log_larger_than_max(tmp_path: Path) -> None:
    log_path = tmp_path / "FortniteGame.log"

    log_path.write_text(
        "A" * 40 + "\n" + "B" * 20 + "\n" + "C" * 20 + "\n",
        encoding="utf-8",
    )

    tailer = FortniteLogTailer(log_path)

    lines = tailer.read_recent_lines(50)

    assert lines == [
        "B" * 20,
        "C" * 20,
    ]

def test_read_recent_lines_does_not_change_position(tmp_path: Path) -> None:
    log_path = tmp_path / "FortniteGame.log"

    log_path.write_text(
        "old line 1\nold line 2\n",
        encoding="utf-8",
    )

    tailer = FortniteLogTailer(log_path)
    tailer.start_at_end()

    recent_lines = tailer.read_recent_lines(10_000)

    assert recent_lines == [
        "old line 1",
        "old line 2",
    ]

    with log_path.open("a", encoding="utf-8") as file:
        file.write("brand new line\n")

    assert tailer.poll() == ["brand new line"]