<script>
  import { onMount } from "svelte";
  import { page } from "$app/state";

  import LineChart from "$lib/LineChart.svelte";
  import Heatmap from "$lib/Heatmap.svelte";
  import StastOverview from "$lib/StastOverview.svelte";

  let sensor_average = $state(null);
  let sensor_record = $state(null);
  let sensor_heatmap = $state(null);
  let loading = $state(true);

  let sensor_id = $derived(page.params.id);

  const retriveData = async (path, id) => {
    try {
      const res = await fetch("http://127.0.0.1:8050/api/device" + path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_name: "device_1" }),
      });

      if (!res.ok) throw new Error(res.status);
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  };

  // 🌿 Derived plant health logic
  const getPlantStatus = (avg) => {
    if (!avg) return "unknown";

    const soil = avg?.soil_moisture?.mean ?? 0;
    const temp = avg?.temperature?.mean ?? 0;

    if (soil < 30) return "dry";
    if (soil > 80) return "overwatered";
    if (temp > 35) return "heat_stress";

    return "healthy";
  };

  onMount(async () => {
    loading = true;

    const [overview, records, heatmap] = await Promise.all([
      retriveData("/overview", sensor_id),
      retriveData("/", sensor_id),
      retriveData("/heatmap", sensor_id),
    ]);

    sensor_average = overview;
    sensor_record = records;
    sensor_heatmap = heatmap;

    loading = false;
  });
</script>

{#if loading}
  <p>Loading plant analytics...</p>
{:else if sensor_record?.raw}
  <div class="dashboard">
    <!-- 🌱 Header -->
    <div class="header">
      <h1>🌿 Plant Sensor Dashboard</h1>
      <h3>Device: {sensor_id}</h3>
      <p>
        Total Records:
        {sensor_record.raw?.length ?? 0}
      </p>

      <p>
        Plant Status:
        <strong>{getPlantStatus(sensor_average)}</strong>
      </p>
    </div>

    <!-- 📊 Overview -->
    <section>
      <h2>Sensor Overview</h2>
      <StastOverview overview={sensor_average} />
    </section>

    <!-- 📈 Trends -->
    <section>
      <h2>Sensor Trends</h2>
      <LineChart series={sensor_record.series} />
    </section>

    <!-- 🔥 Heatmap -->
    {#if sensor_heatmap}
      <section>
        <h2>Soil & Environmental Heatmap</h2>
        <Heatmap heatmap_data={sensor_heatmap} />
      </section>
    {/if}
  </div>
{:else}
  <p>No sensor data available.</p>
{/if}

<style></style>
