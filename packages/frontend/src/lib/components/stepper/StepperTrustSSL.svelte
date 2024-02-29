<script lang="ts">
    import { createStepController } from "@efstajas/svelte-stepper";
    import Button from "../Button.svelte";
    import Icon from "@iconify/svelte";
    import { IP_ADDRESS } from "$lib/utils/settings";

    let hasTrustedSSL = false;

    const stepController = createStepController();
</script>

<div class="flex flex-col gap-4">
    <h1 class="text-2xl font-serif">MIA Connect Zertifikat vertrauen</h1>
    <p>
        MIA Connect verwendet ein dynamisches SSL Zertifikat. Bitte vertraue dem
        Zertifikat, um eine sichere Verbindung herzustellen.
    </p>
    <p>
        <span class="font-semibold">Hinweis:</span> Das Zertifikat wird nur temporär
        vertraut und muss bei jedem Neustart des Fahrzeugs erneut bestätigt werden.
    </p>
    <div class="mt-4">
        <button
            class="border-b-2 transition-all duration-300 border-transparent hover:border-blue-300 border-dashed px-1 py-1 font-semibold flex items-center gap-2 w-fit"
            on:click={() => {
                const popup = window.open(
                    `https://${IP_ADDRESS}:1606/ssl.html`,
                    "_blank",
                    "width=600,height=600",
                );
                window.addEventListener("message", (event) => {
                    if (event.data == "success") {
                        popup?.close();
                        hasTrustedSSL = true;
                    }
                });
            }}
        >
            <Icon class="text-blue-500" icon="mdi:arrow-right" />
            <span> Zertifikat vertrauen </span></button
        >
    </div>
    <div class="flex justify-between mt-8">
        <Button
            label="Zurück"
            style="default"
            onClick={stepController.previousStep}
        />
        <Button
            label="Fortfahren"
            style="default"
            disabled={!hasTrustedSSL}
            onClick={stepController.nextStep}
        />
    </div>
</div>
