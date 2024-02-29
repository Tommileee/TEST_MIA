<script lang="ts">
    import { createStepController } from "@efstajas/svelte-stepper";
    import { socket, isConnected } from "$stores/socket";
    import toast from "svelte-french-toast";
    import Button from "../Button.svelte";
    import { IP_ADDRESS } from "$lib/utils/settings";
    const stepController = createStepController();

    function connect() {
        let connectPromise = new Promise<void>((resolve, reject) => {
            $socket = new WebSocket(`wss://${IP_ADDRESS}:1606/websocket`);

            $socket.onopen = () => {
                isConnected.set(true);
                resolve();
            };
            $socket.onclose = () => {
                isConnected.set(false);

                toast.error("Verbindung getrennt!");
            };
            $socket.onerror = () => {
                isConnected.set(false);
                reject(new Error("Connection Error"));
            };
        });

        toast.promise(connectPromise, {
            loading: "Verbindung wird hergestellt...",
            success: "Die Verbindung wurde hergestellt!",
            error: "Es konnte keine Verbindung hergestellt werden!",
        });
    }
</script>

<div class="flex flex-col gap-4">
    <h1 class="text-2xl font-serif">Fertig!</h1>
    <p>
        Du kannst nun die Verbindung zu <span
            class="font-semibold text-blue-500">MIA</span
        >
        herstellen.
    </p>
    <div class="flex justify-between mt-8">
        <Button
            label="Zurück"
            style="default"
            onClick={stepController.previousStep}
        />
        <Button
            label="Verbindung herstellen"
            style="primary"
            onClick={connect}
        />
    </div>
</div>
