import { AiSocketService } from "./src/service/ai-socket.service";
import { GameRecordService } from "./src/service/game-record.service";
import WebSocket from "ws";
import { dataToSend, expectedResponse } from "./src/socket-data";

(globalThis as any).WebSocket = WebSocket;
(globalThis as any).localStorage = {
  storage: {
    jwtToken: "test-jwt-token",
  } as Record<string, string>,
  getItem(key: string) {
    return this.storage[key] || null;
  },
};

const args = process.argv.slice(2);

const interval = args[0] ? parseInt(args[0]) : 1000;
const socketMaxOpenTime = args[1] ? parseInt(args[1]) : 3000;
const updateTimestamp = args[2] ? args[2].toLowerCase() === "true" : false;
const customDataToSendFieldsSequence: Record<string, any>[] = args[3]
  ? JSON.parse(args[3])
  : null;

let sequenceIndex = 0;

const socketUrl = "http://localhost:8000/ws/test/";
const aiSocketService = new AiSocketService();
const gameRecordService = new GameRecordService();

function getDataFromGame() {
  const newDataToSend = dataToSend;

  if (updateTimestamp) {
    newDataToSend.state.timestamp = Date.now();
  }

  if (customDataToSendFieldsSequence.length > 0) {
    const fields =
      customDataToSendFieldsSequence[
        sequenceIndex % customDataToSendFieldsSequence.length
      ];
    for (const [key, value] of Object.entries(fields)) {
      newDataToSend.state[key] = value;
    }
    sequenceIndex++;
  }

  return newDataToSend;
}

function main() {
  const currentGameStateData = getDataFromGame();
  aiSocketService.dataToSend = currentGameStateData;
  gameRecordService.currentData = currentGameStateData;

  aiSocketService.connect(
    socketUrl,
    () => {
      console.log("Client connected!");

      aiSocketService.startDataExchange(interval, expectedResponse, 0);

      setTimeout(() => {
        console.log("Closing socket...");
        aiSocketService.closeSocket();
      }, socketMaxOpenTime);
    },
    (event) => {
      console.log("Received from server:", event.data);

      const currentGameStateData = getDataFromGame();
      aiSocketService.dataToSend = currentGameStateData;
      gameRecordService.currentData = currentGameStateData;
    },
    (e: unknown) => {
      console.error("Connection error: ", e);
    },
    () => {
      console.log("Socket closed.");
      gameRecordService.sendDataset();
    }
  );
}

main();
