import { writable } from "svelte/store";

export type DrivingMode = "simple" | "advanced";
export const drivingMode = writable<DrivingMode>("simple");