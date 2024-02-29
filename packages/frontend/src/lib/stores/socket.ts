import { writable } from "svelte/store";

export const socket = writable<WebSocket | null>(null);
export const isConnected = writable<boolean>(false);