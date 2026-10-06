from pypresence.presence import Presence


class DiscordRPC:
    def __init__(self, application_id: str) -> None:
        self.rpc = Presence(application_id)

    def connect(self) -> None:
        self.rpc.connect()

    def update(self, details: str, state_text: str) -> None:
        self.rpc.update(details=details, state=state_text)

    def clear(self) -> None:
        self.rpc.clear()
