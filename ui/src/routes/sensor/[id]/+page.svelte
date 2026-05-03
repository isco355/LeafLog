<script>
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import LineChart from "$lib/LineChart.svelte";
  import Heatmap from "$lib/Heatmap.svelte";
  import StastOverview from "$lib/StastOverview.svelte";
  import RecordCard from "$lib/recordCard.svelte";
  let sensor_average = $state({});
  let sensor_record = $state({});
  let sensor_analyzer = $state(null);

  let sensor_id = $derived(page.params.id);

  const retriveData = (path, id) => {
    const config = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device_name: id }),
    };

    return fetch("http://127.0.0.1:8050/api/device" + path, config)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP error ${r.status}`);
        return r.json();
      })
      .catch((e) => console.error(e));
  };

  onMount(async () => {
    const overview = await retriveData("/overview", sensor_id);
    sensor_average = overview ?? {};

    const records = await retriveData("/", sensor_id);
    sensor_record = records ?? {};

    const heatmap = await retriveData("/analyzer", sensor_id);
    sensor_analyzer = heatmap ?? {};
    console.log(sensor_record);
  });
</script>

{#if Object.hasOwn(sensor_record, "raw")}
  <h3 class="text-2xl font-bold">
    Device Name: {sensor_id}, total records: {sensor_record["raw"].length}
  </h3>
{/if}
{#if sensor_analyzer}
  <div class="flex flex-row gap-2">
    <div class="flex flex-col w-1/2 gap-2 overflow-auto">
      <h1>LOGS</h1>
      {#each sensor_record["raw"] as record_data}
        <RecordCard record={record_data} />
      {/each}
    </div>
    <div>
      <StastOverview overview={sensor_average} />
      <LineChart series={sensor_record["series"]} />
      <Heatmap heatmap_data={sensor_analyzer["heatmap"]} />
      <Heatmap heatmap_data={sensor_analyzer["correlation"]} />
    </div>
  </div>
{/if}
