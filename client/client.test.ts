import { AiSocketService } from "./ai-socket.service";
import WebSocket from "ws";
import { ISocketData } from "./ISocketData";

(globalThis as any).WebSocket = WebSocket;

(globalThis as any).localStorage = {
  storage: {} as Record<string, string>,
  getItem(key: string) {
    return this.storage[key] || null;
  },
};

const service = new AiSocketService();

const socketUrl = "http://localhost:8000/ws/test/";
const dataToSend: ISocketData = {
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
const expectedResponse = { move: -1 };

service.dataToSend = dataToSend;

service.connect(
  socketUrl,
  () => {
    console.log("Client connected!");

    service.startDataExchange(1000, expectedResponse, 0);

    setTimeout(() => {
      console.log("Closing socket...");
      service.closeSocket();
    }, 6000);
  },
  (event) => {
    console.log("Received from server:", event.data);
  },
  (e: unknown) => {
    console.error("Connection error: ", e);
  },
  () => {
    console.log("Socket closed.");
  }
);
