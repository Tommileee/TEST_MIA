<script lang="ts">
    import SimpleJoystick from "./joysticks/SimpleJoystick.svelte";
    import AdvancedJoystick from "./joysticks/AdvancedJoystick.svelte";
    import Icon from "@iconify/svelte";
    import { drivingMode } from "$stores/mia";
    import { Modal, Button, Input, Label, Helper } from "flowbite-svelte";
    import { socket } from "$lib/stores/socket";
    import toast from "svelte-french-toast";

    const video_stream = "https://c.tenor.com/m9EKZvs_M8QAAAAd/tenor.gif";

    function sendTTS() {
        $socket?.send(JSON.stringify({ topic: "TTS", payload: ttsText }));
        toast.success("Text wird gesprochen!");
    }

    let ttsText = "";

    let ttsModal = false;
    let aiActive = false;

    let compileTime = new Date(__COMPILE_TIME__);
</script>

<div class="flex-grow flex flex-col min-h-dvh">
    <header class="py-4 px-8 font-serif flex justify-between items-center">
        <div class="flex flex-col">
            <span class="text-4xl">MIA</span>
            <span class="text-xs"> Mercedes Intelligent Assistant</span>
        </div>
        <div>
            <div class="flex gap-2 items-center">
                <span class="font-mono text-sm text-neutral-500"
                    >{compileTime.toLocaleString("de", {
                        timeZone: "Europe/Berlin",
                    })} | {__VERSION_SLUG__}</span
                >
                <div
                    class="bg-green-500 w-4 h-4 rounded-full animate-pulse"
                ></div>
            </div>
        </div>
    </header>
    <main
        class="flex-grow px-8 py-4 flex flex-row items-center justify-center gap-64"
    >
        <div class="relative select-none pointer-events-none">
            <img
                src={video_stream}
                alt="Video Stream"
                class="rounded-lg w-[640px] h-[480px] object-cover"
            />
        </div>
        <div class="w-96">
            {#if $drivingMode == "simple"}
                <SimpleJoystick />
            {:else}
                <AdvancedJoystick />
            {/if}
        </div>
    </main>
    <div class="px-8 py-4">
        <ul class="flex flex-wrap gap-4">
            <li>
                <button
                    on:click={() => drivingMode.set("simple")}
                    class="gap-2 flex items-center hover:bg-black/10 hover:cursor-pointer rounded-md px-4 py-2"
                >
                    <Icon icon="mdi:car" />
                    <span class="font-semibold">Einfacher Modus</span>
                </button>
            </li>
            <li>
                <button
                    on:click={() => drivingMode.set("advanced")}
                    class="gap-2 flex items-center hover:bg-black/10 hover:cursor-pointer rounded-md px-4 py-2"
                >
                    <Icon icon="mdi:car-sports" />
                    <span class="font-semibold">Fortgeschrittener Modus</span>
                </button>
            </li>
            <li>
                <Modal title="Text-to-Speech" bind:open={ttsModal} autoclose>
                    <div>
                        <Label for="tts" class="mb-2">Text</Label>
                        <Input
                            type="text"
                            id="tts"
                            required
                            bind:value={ttsText}
                        />
                    </div>
                    <svelte:fragment slot="footer">
                        <Button on:click={() => sendTTS()}>Sprechen</Button>
                        <Button color="alternative">Abbrechen</Button>
                    </svelte:fragment>
                </Modal>
                <button
                    on:click={() => (ttsModal = true)}
                    class="gap-2 flex items-center hover:bg-black/10 hover:cursor-pointer rounded-md px-4 py-2"
                >
                    <Icon icon="mdi:speak" />
                    <span class="font-semibold">Text-to-Speech</span>
                </button>
            </li>
            <li>
                <button
                    class="gap-2 flex items-center hover:bg-black/10 hover:cursor-pointer rounded-md px-4 py-2"
                    disabled={aiActive}
                    on:click={() => {
                        aiActive = true;
                        $socket?.send(
                            JSON.stringify({
                                topic: "ai",
                                payload: { active: true },
                            }),
                        );
                        toast.success("AI wird aktiviert!");
                    }}
                >
                    <Icon icon="mdi:sparkles" />
                    <span class="font-semibold">AI</span>
                </button>
            </li>
        </ul>
    </div>
</div>
