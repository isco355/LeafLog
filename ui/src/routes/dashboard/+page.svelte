<script>
  import { onMount } from "svelte";
  import "../../app.css";
  import SensorCard from "$lib/sensorCard.svelte";
  import StastOverview from "$lib/StastOverview.svelte";
  import Simulated from "$lib/simulated.svelte";
  import { getDevices } from "$lib/network";

  let data = $state([]);
  let error = null;

  onMount(async () => {
    data = await getDevices();
  });
</script>

<div class="p-4">
  {#if error}
    <p class="text-red-500">{error}</p>
  {:else if data.length === 0}
    <Simulated />
  {:else}
    <StastOverview
      title={"All Sensors Summarize"}
      overview={data["overview"]}
    />

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {#each data["records"] as sensor_data}
        <SensorCard sensor={sensor_data} />
      {/each}
    </div>
  {/if}
</div>
