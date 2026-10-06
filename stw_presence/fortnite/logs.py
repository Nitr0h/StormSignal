import os
from pathlib import Path


def get_fortnite_log_path() -> Path:
    local_app_data = os.environ["LOCALAPPDATA"]

    return Path(local_app_data) / "FortniteGame" / "Saved" / "Logs" / "FortniteGame.log"


class FortniteLogTailer:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._position = 0

    def start_at_end(self) -> None:
        with self._path.open("rb") as file:
            file.seek(0, 2)
            self._position = file.tell()

    def poll(self) -> list[str]:
        decoded_lines: list[str] = []

        file_size = self._path.stat().st_size

        if file_size < self._position:
            self._position = 0

        with self._path.open("rb") as file:
            file.seek(self._position)

            for line in file.readlines():
                decoded_line = line.decode(
                    "utf-8",
                    errors="replace",
                ).rstrip()

                decoded_lines.append(decoded_line)

            self._position = file.tell()

        return decoded_lines

    def read_recent_lines(self, max_bytes: int) -> list[str]:
        with self._path.open("rb") as file:
            decoded_lines: list[str] = []
            file_size: int = self._path.stat().st_size
            start_position: int = max(0, file_size - max_bytes)

            file.seek(start_position)

            if start_position > 0:
                file.seek(start_position - 1)

                if file.read(1) != b"\n":
                    file.readline()

            for line in file.readlines():
                decoded_line = line.decode(
                    "utf-8",
                    errors="replace",
                ).rstrip()

                decoded_lines.append(decoded_line)

        return decoded_lines
