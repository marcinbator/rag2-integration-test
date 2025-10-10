export interface GameState {
  name: string;
  playerId: number;
  state: Record<string, any>;
  players: any[];
  expectedInput: Record<string, any>;
  timestamp?: number;
}

//

export const dataToSend: GameState = {
  playerId: 0,
  state: {
    leftPaddleY: 225,
    rightPaddleY: 185,
    leftPaddleSpeed: 0,
    rightPaddleSpeed: -20,
    ballX: 508,
    ballY: 304,
    ballSpeedX: 8,
    ballSpeedY: 4,
    timestamp: Date.now(),
  },
  players: [
    {
      inputData: {
        move: 0,
        start: 0,
      },
      expectedDataDescription: "string",
      isObligatory: true,
      id: 0,
      isActive: true,
      name: "player 1",
      playerType: "SOCKET",
    },
  ],
  expectedInput: {
    move: 0,
    start: 0,
  },
  name: "pong",
};

export const expectedResponse = { move: -1 };
