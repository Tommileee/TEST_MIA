<script lang="ts">
    export let label: string;
    export let style: "default" | "primary" = "default";
    export let onClick: () => void;
    export let disabled: boolean = false;

    let styleClasses = {
        default: "bg-neutral-100",
        primary: "bg-blue-200 border-blue-400 text-black",
    };
</script>

<button
    class="px-4 py-2 {styleClasses[
        style
    ]} border rounded-md font-semibold disabled:opacity-20 disabled:cursor-not-allowed"
    on:click={() => onClick()}
    {disabled}>{label}</button
>
