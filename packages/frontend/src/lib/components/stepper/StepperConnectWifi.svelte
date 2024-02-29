<script lang="ts">
    import { createStepController } from "@efstajas/svelte-stepper";
    import Button from "../Button.svelte";

    const stepController = createStepController();
    let compileTime = new Date(__COMPILE_TIME__);
</script>

<div class="flex flex-col gap-4">
    <h1 class="text-2xl font-serif">Mit WLAN verbinden</h1>
    <p>
        Zum Steuern des Fahrzeugs ist eine direkte Verbindung notwendig. Bitte
        verbinde dich mit dem <span class="text-blue-500 font-semibold"
            >MIA Connect</span
        >
        WLAN und drücke anschließend auf
        <span class="text-blue-500 font-semibold">"Fortfahren"</span>.
    </p>
    <ol class="flex flex-col gap-4">
        <li class="flex flex-col">
            <span class="font-serif">SSID </span>
            <span class="text-lg font-mono"> MIA Connect</span>
        </li>
        <li class="flex flex-col">
            <span class="font-serif flex gap-2 items-center">PSK</span>
            <span class="text-lg font-mono">miaconnect</span>
        </li>
    </ol>
    <div class="flex justify-between items-center">
        <span class="font-mono text-sm text-neutral-500"
            >{compileTime.toLocaleString("de", {
                timeZone: "Europe/Berlin",
            })} | {__VERSION_SLUG__}</span
        >
        <Button
            label="Fortfahren"
            style="default"
            onClick={stepController.nextStep}
        />
    </div>
</div>
