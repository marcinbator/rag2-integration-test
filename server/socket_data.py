from typing import Any

from pydantic import BaseModel


class SocketPlayer(BaseModel):
    inputData: dict[str, Any]
    expectedDataDescription: str
    isObligatory: bool
    id: int
    isActive: bool
    name: str
    playerType: str


class SocketData(BaseModel):
    name: str
    playerId: int
    state: dict[str, Any]
    players: list[SocketPlayer]
    expectedInput: dict[str, Any]
