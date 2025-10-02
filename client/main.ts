import { AiSocketService } from "./src/service/ai-socket.service";
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

const socketUrl = "http://localhost:8000/ws/test/";
const service = new AiSocketService();

function main() {
  service.dataToSend = dataToSend;

  service.connect(
    socketUrl,
    () => {
      console.log("Client connected!");

      service.startDataExchange(interval, expectedResponse, 0);

      setTimeout(() => {
        console.log("Closing socket...");
        service.closeSocket();
      }, socketMaxOpenTime);
    },
    (event) => {
      console.log("Received from server:", event.data);
      const newDataToSend = dataToSend;
      if (updateTimestamp) {
        newDataToSend.state.timestamp = Date.now();
      }
      service.dataToSend = newDataToSend;
    },
    (e: unknown) => {
      console.error("Connection error: ", e);
    },
    () => {
      console.log("Socket closed.");
    }
  );
}

main();
