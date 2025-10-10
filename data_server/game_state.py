from typing import Any

from pydantic import BaseModel


class GameState(BaseModel):
    name: str
    playerId: int
    state: dict[str, Any]
    players: list[Any]
    expectedInput: dict[str, Any]
