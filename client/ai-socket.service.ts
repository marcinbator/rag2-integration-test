import { AuthEndpointsServiceMock } from "./auth-endpoint.mock.service";
import { ISocketData } from "./ISocketData";

export class AiSocketService {
  private readonly _INACTIVITY_TIMEOUT = 60000;

  private _socket!: WebSocket | null;
  private _isSocketConnected = false;
  private _sendingIntervalID: unknown | null = null;
  private _isDataSendingActive = false;
  private _previousData = "";
  private _ping = 0;
  private _lastPingSentTime = 0;
  private _inactivityTimeoutID: ReturnType<typeof setTimeout> | null = null;
  private _authEndpointsService = new AuthEndpointsServiceMock();
  private _dataToSend!: ISocketData;
  private _isDataExchangeDesired = false;

  public set dataToSend(data: ISocketData) {
    this._dataToSend = data;
  }

  public connect(
    socketUrl: string,
    onOpen: () => void,
    onMessage: (event: MessageEvent<string>) => void,
    onError: (e: unknown) => void,
    onClose: () => void
  ): void {
    this._authEndpointsService.verifyJWTToken().subscribe({
      next: (isValid: boolean) => {
        if (isValid) {
          socketUrl = `${socketUrl}?jwt=${localStorage.getItem("jwtToken")}`;
        }
        this.defineSocket(socketUrl, onOpen, onMessage, onError, onClose);
      },
      error: () => {
        console.log("Error verifying JWT token. Opening as guest.");
        this.defineSocket(socketUrl, onOpen, onMessage, onError, onClose);
      },
    });
  }

  public startDataExchange = (
    sendingInterval: number,
    expectedDataToReceive: Record<string, unknown>,
    playerId: number
  ): void => {
    this._isDataExchangeDesired = true;
    this.resumeDataExchange(sendingInterval, expectedDataToReceive, playerId);
  };

  public pauseDataExchange = (): void => {
    if (!this._sendingIntervalID) return;

    this._isDataSendingActive = false;
    clearInterval(this._sendingIntervalID as number);
  };

  public resumeDataExchange = (
    sendingInterval: number,
    expectedDataToReceive: Record<string, unknown>,
    playerId: number
  ): void => {
    if (!this._isDataExchangeDesired) return;

    this._isDataSendingActive = true;

    this._sendingIntervalID = setInterval(() => {
      this.sendDataToSocket(this._dataToSend, expectedDataToReceive, playerId);
      this._lastPingSentTime = Date.now();
    }, sendingInterval);
  };

  public stopDataExchange = (): void => {
    this._isDataExchangeDesired = false;
    this.pauseDataExchange();
  };

  public closeSocket(): void {
    if (this._socket) {
      this._socket.close();
      this._socket = null;
    }
  }

  //

  private defineSocket(
    socketUrl: string,
    onOpen: () => void,
    onMessage: (event: MessageEvent<string>) => void,
    onError: (e: unknown) => void,
    onClose: () => void
  ): void {
    this._socket = new WebSocket(socketUrl);
    this._socket.addEventListener("open", () => {
      this._isSocketConnected = true;
      onOpen();
      this.resetInactivityTimeout();
    });
    this._socket.addEventListener("error", (e) => {
      onError(e);
      this.resetInactivityTimeout();
    });
    this._socket.addEventListener("message", (event) => {
      onMessage(event);
      this._ping = Date.now() - this._lastPingSentTime;
      this.resetInactivityTimeout();
    });
    this._socket.addEventListener("close", (e) => {
      if (e.code === 401) {
        console.log(
          "Max guest users limit reached. Log in to play or try again later."
        );
      }

      this.stopDataExchange();

      this._isSocketConnected = false;
      this._previousData = "";
      this._ping = 0;
      this._lastPingSentTime = 0;

      this.clearInactivityTimeout();

      onClose();
    });
  }

  private sendDataToSocket(
    dataToSend: ISocketData,
    expectedDataToReceive: Record<string, unknown>,
    playerId: number
  ): void {
    if (this._socket && this._isSocketConnected) {
      const data: string = JSON.stringify({
        name: dataToSend["name"],
        playerId: playerId,
        state: dataToSend["state"],
        players: dataToSend["players"],
        expectedInput: expectedDataToReceive,
      });

      if (data != this._previousData) {
        this._socket.send(data);
        this.resetInactivityTimeout();
      }

      this._previousData = data;
    }
  }

  private resetInactivityTimeout(): void {
    if (this._inactivityTimeoutID) {
      clearTimeout(this._inactivityTimeoutID);
    }
    this._inactivityTimeoutID = setTimeout(() => {
      console.log("No activity detected. Closing WebSocket connection.");
      this.closeSocket();
    }, this._INACTIVITY_TIMEOUT);
  }

  private clearInactivityTimeout(): void {
    if (!this._inactivityTimeoutID) return;

    clearTimeout(this._inactivityTimeoutID);
    this._inactivityTimeoutID = null;
  }
}
