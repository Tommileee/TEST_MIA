<script lang="ts">
    import { Stepper, makeStep } from "@efstajas/svelte-stepper";
    import Dashboard from "./lib/components/Dashboard.svelte";
    import { Toaster } from "svelte-french-toast";
    import StepperConnectWifi from "./lib/components/stepper/StepperConnectWifi.svelte";
    import StepperTrustSSL from "./lib/components/stepper/StepperTrustSSL.svelte";
    import StepperConnectMia from "./lib/components/stepper/StepperConnectMia.svelte";

    import { isConnected } from "./lib/stores/socket";

    const steps = [
        makeStep({
            component: StepperConnectWifi,
            props: undefined,
        }),
        makeStep({
            component: StepperTrustSSL,
            props: undefined,
        }),
        makeStep({
            component: StepperConnectMia,
            props: undefined,
        }),
    ];
</script>

{#if !$isConnected}
    <div
        class="absolute flex min-h-dvh bg-gradient-to-br from-neutral-100 via-neutral-100 to-neutral-50 w-dvw z-40 justify-center items-center backdrop-blur-md"
    >
        <div class="bg-white rounded-md w-1/3 px-6 py-8 shadow-lg border">
            <Stepper {steps} />
        </div>
    </div>
{:else}
    <div class="flex min-dvh flex-col">
        <Dashboard />
    </div>
{/if}

<Toaster />
