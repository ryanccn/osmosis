import { io } from "socket.io-client";

export const ws = io({ timeout: 60000 });
