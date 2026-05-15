<script>
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import LineChart from "$lib/LineChart.svelte";
  import Heatmap from "$lib/Heatmap.svelte";
  import StastOverview from "$lib/StastOverview.svelte";
  import RecordCard from "$lib/recordCard.svelte";
  import { retriveData } from "$lib/network.ts";

  let sensor_average = $state({});
  let sensor_record = $state({});
  let sensor_analyzer = $state(null);

  let sensor_id = $derived(page.params.id);

  onMount(async () => {
    sensor_average = await retriveData("/overview", sensor_id);

    const records = await retriveData("/", sensor_id);
    sensor_record = records ?? {};

    const heatmap = await retriveData("/analyzer", sensor_id);
    sensor_analyzer = heatmap ?? {};
  });
</script>

{#await sensor_average}
  <p>loading</p>
{:then value}
  {#if sensor_analyzer}
    <div class="flex flex-colum gap-20 items-center justify-center">
      <div class="flex flex-col gap-10">
        <StastOverview
          title={`Sensor Overview: ${sensor_id}`}
          overview={sensor_average}
        />

        <h1 class="text-xl font-bold text-center">
          Total Records: {sensor_record["raw"].length}
        </h1>
        <LineChart series={sensor_record["series"]} />
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#each sensor_analyzer["heatmap"] as heatmap_data}
            <Heatmap {heatmap_data} />
          {/each}
        </div>
        <div class="flex flex-col w-2/5 gap-2 overflow-auto">
          <!-- <h1 class="text-xl font-bold text-center"> -->
          <!--   Total Records: {sensor_record["raw"].length} -->
          <!-- </h1> -->
          <!-- {#each sensor_record["raw"] as record_data} -->
          <!--   <RecordCard record={record_data} /> -->
          <!-- {/each} -->
        </div>
      </div>
    </div>
  {/if}
{/await}
