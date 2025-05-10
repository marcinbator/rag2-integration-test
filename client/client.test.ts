import {AiSocketService} from "./ai-socket.service";
import WebSocket from "ws";

(globalThis as any).WebSocket = WebSocket;

(globalThis as any).localStorage = {
    storage: {} as Record<string, string>,
    getItem(key: string) {
        return this.storage[key] || null;
    },
};

const service = new AiSocketService();

const socketUrl = "http://localhost:8000/ws/test/";
const dataToSend = {
    playerId: 0,
    state: {
        ballY: 20,
        leftPaddleY: 50,
        rightPaddleY: 20
    },
};
const expectedResponse = {move: -1};

service.setDataToSend(dataToSend);

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
