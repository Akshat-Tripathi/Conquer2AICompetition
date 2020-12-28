from .websockets import send, recv

class conquer2_adapter:
    def __init__(self, username: str, password: str, code: str) -> None:
        return self.login(username, password, code)
    
    def login(self, username: str, password: str, code: str) -> bool:
        return False

    def start(self) -> None:
        ...

    def send_command(self, action) -> None:
        ...

    def get_state(self) -> list[list]:
        ...