<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import NippleJS from "nipplejs";
    import { socket } from "$lib/stores/socket";
    import { IP_ADDRESS } from "$lib/utils/settings";

    let joystickDiv: HTMLDivElement;
    let lastValue: number[] = [0, 0];
    let currentValue: number[] = [0, 0];
    let communicationInterval: number;

    onMount(() => {
        const options = {
            zone: joystickDiv, // active zone
            color: "black",
            size: 350,
            mode: "static" as const,
            shape: "square" as const,
            position: { left: "50%", top: "50%" },
        };
        const manager = NippleJS.create(options);

        manager.on("move", function (evt, nipple) {
            const { x, y } = nipple.vector;
            const direction = Math.round(255 * x);
            const speed = Math.round(255 * y);

            currentValue = [speed, direction];
        });

        manager.on("end", function () {
            currentValue = [0, 0];
        });

        communicationInterval = setInterval(() => {
            if (lastValue === currentValue) return;

            lastValue = currentValue;

            fetch(`https://${IP_ADDRESS}:1606/api/driving-simple`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    speed: lastValue[0],
                    direction: lastValue[1],
                    now: new Date().getTime() / 1000,
                }),
            });

            /*
            $socket?.send(
                JSON.stringify({
                    topic: "driving-simple",
                    payload: {
                        speed: lastSentValue[0],
                        direction: lastSentValue[1],
                    },
                }),
            );*/
        }, 300);
    });

    onDestroy(() => {
        clearInterval(communicationInterval);
    });
</script>

<div class="z-0 border-2 border-dashed aspect-square w-96 rounded-md relative">
    <div bind:this={joystickDiv} class="joystick z-0"></div>
</div>
