export interface ISocketPlayer {
    inputData: Record<string, any>;
    expectedDataDescription: string;
    isObligatory: boolean;
    id: number;
    isActive: boolean;
    name: string;
    playerType: string;
}

export interface ISocketData {
    name: string;
    playerId: number;
    state: Record<string, any>;
    players: ISocketPlayer[];
    expectedInput: Record<string, any>;
}
