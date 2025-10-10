import { GameState } from "../socket-data";

export class GameRecordService {
  private _dataSet: GameState[] = [];
  private readonly DATA_SERVER_URL = "http://localhost:8080/game-states";

  public set currentData(data: GameState) {
    this._dataSet.push(data);
  }

  public async sendDataset(): Promise<void> {
    const response = await fetch(this.DATA_SERVER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        dataset: this._dataSet,
        timestamp: new Date().toISOString(),
        totalRecords: this._dataSet.length,
      }),
    });

    if (response.ok) {
      const result = await response.json();
      console.log("Data sent successfully");
    } else {
      console.error(
        "Failed to send data:",
        response.status,
        response.statusText
      );
    }
  }
}
