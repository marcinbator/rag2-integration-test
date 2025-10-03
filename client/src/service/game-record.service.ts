import { ISocketData } from "../socket-data";

export class GameRecordService {
  private _dataSet: ISocketData[] = [];
  private readonly DATA_SERVER_URL = "http://localhost:8080/data";

  public set currentData(data: ISocketData) {
    this._dataSet.push(data);
  }

  public async sendDataset(): Promise<void> {
    if (this._dataSet.length === 0) {
      console.log("No data to send");
      return;
    }

    try {
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
        console.log("Data sent successfully:", result);
      } else {
        console.error(
          "Failed to send data:",
          response.status,
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error sending data to server:", error);
    }
  }
}
