<script lang="ts">
    import ControllerImage from "$assets/controller.jpg";
    import { socket } from "$lib/stores/socket";
    import { IP_ADDRESS } from "$lib/utils/settings";
    import { onDestroy, onMount } from "svelte";

    let motorLeft: number = 0,
        motorRight: number = 0;
    $: currentValue = [motorLeft, motorRight];
    let communicationInterval: number;
    let lastValue: number[] = [0, 0];

    function pollGamepads() {
        const gamepads = navigator.getGamepads();
        for (const gamepad of gamepads) {
            if (!gamepad || gamepad?.id?.toLowerCase().includes("unknown")) {
                continue;
            }

            const axes = gamepad.axes;

            const leftStickY = axes[1] * -1;
            const rightStickY = axes[3] * -1; // * -1 because the y-axis is inverted

            let roundedLeftStickY = Math.round(leftStickY * 100) / 100;
            let roundedRightStickY = Math.round(rightStickY * 100) / 100;

            // If value is between -0.1 and 0.1, we consider it as 0
            if (roundedLeftStickY >= -0.25 && roundedLeftStickY <= 0.25) {
                roundedLeftStickY = 0;
            }
            if (roundedRightStickY >= -0.25 && roundedRightStickY <= 0.25) {
                roundedRightStickY = 0;
            }

            // If value is between -1.0 and -0.9, we consider it as -1
            if (roundedLeftStickY >= -1.0 && roundedLeftStickY <= -0.9) {
                roundedLeftStickY = -1;
            }
            if (roundedRightStickY >= -1.0 && roundedRightStickY <= -0.9) {
                roundedRightStickY = -1;
            }

            motorLeft = Math.round(roundedLeftStickY * 255);
            motorRight = Math.round(roundedRightStickY * 255);
        }
        requestAnimationFrame(pollGamepads);
    }

    onMount(() => {
        pollGamepads();

        communicationInterval = setInterval(() => {
            if (lastValue == currentValue) return;

            lastValue = currentValue;

            fetch(`https://${IP_ADDRESS}:1606/api/driving-advanced`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    motor_left: lastValue[0],
                    motor_right: lastValue[1],
                    now: new Date().getTime() / 1000,
                }),
            });
            /*$socket?.send(
                JSON.stringify({
                    topic: "driving-advanced",
                    payload: {
                        motor_left: lastValue[0],
                        motor_right: lastValue[1],
                    },
                }),
            );*/
        }, 300);
    });

    onDestroy(() => {
        clearInterval(communicationInterval);
    });
</script>

<div>
    <img src={ControllerImage} alt="PS5 Controller" />
    <p>Bitte verwende nun deinen Controller zur Steuerung.</p>
</div>
