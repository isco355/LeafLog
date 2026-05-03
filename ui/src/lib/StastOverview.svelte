<script>
  import {
    Battery,
    Droplets,
    Signal,
    Sprout,
    Thermometer,
  } from "lucide-svelte";

  const { overview } = $props();

  const formatLabel = (key) =>
    key.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());

  const icons = {
    battery: Battery,
    humidity: Droplets,
    linkquality: Signal,
    soil_moisture: Sprout,
    temperature: Thermometer,
  };
</script>

<main>
  <h1>Sensor Overview</h1>

  <div class="grid">
    {#each Object.entries(overview) as [key, value]}
      <div class="card">
        <div class="header">
          <div class="icon">
            <svelte:component this={icons[key]} size="22" />
          </div>
          <h2>{formatLabel(key)}</h2>
        </div>

        <div class="stats">
          <div>
            <span>Min</span>
            <strong>{value.min}</strong>
          </div>
          <div>
            <span>Mean</span>
            <strong>{value.mean}</strong>
          </div>
          <div>
            <span>Max</span>
            <strong>{value.max}</strong>
          </div>
        </div>
      </div>
    {/each}
  </div>
</main>

<style>
  main {
    font-family: system-ui, sans-serif;
    padding: 2rem;
    /* background: #f5f7fa; */
    min-height: 100px;
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 600;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
  }

  .card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    transition: transform 0.15s ease;
  }

  .card:hover {
    transform: translateY(-4px);
  }

  .header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
  }

  .icon {
    color: black;
  }

  h2 {
    font-size: 1.1rem;
    color: #333;
  }

  .stats {
    display: flex;
    justify-content: space-between;
  }

  .stats div {
    text-align: center;
  }

  span {
    display: block;
    font-size: 0.75rem;
    color: #888;
  }

  strong {
    font-size: 1.2rem;
    color: #222;
  }
</style>
