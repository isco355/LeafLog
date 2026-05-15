<script>
  import {
    Activity,
    Thermometer,
    Droplets,
    Sprout,
    Gauge,
    Clock,
  } from "lucide-svelte";
  const { sensor } = $props();

  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };

  const prettyTime = (timestamp) => {
    const new_date = new Date(timestamp);
    return new_date.toLocaleString("en-US", options);
  };
</script>

<a href="/dashboard/sensor/{sensor.device_name}" class="block group">
  <div
    class="rounded-3xl border border-outline-variant/30 overflow-hidden
           bg-gradient-to-br from-surface-container-lowest to-surface-container-low
           shadow-sm hover:shadow-xl transition-all duration-300"
  >
    <div class="p-6 flex items-start justify-between">
      <div class="space-y-1">
        <div class="flex items-center gap-2 text-primary">
          <Activity size="18" />
          <span class="text-xs uppercase tracking-widest text-stone-400">
            Sensor
          </span>
        </div>

        <h3 class="text-lg font-bold text-on-surface">
          {sensor.device_name}
        </h3>

        <div class="flex items-center gap-2 text-xs text-stone-400">
          <Clock size="14" />
          <span>{prettyTime(sensor.ts)}</span>
        </div>
      </div>

      <div class="relative">
        <div
          class="absolute inset-0 rounded-full animate-pulse bg-emerald-500/10"
        />
      </div>
    </div>

    <div class="px-6 pb-4"></div>

    <div class="px-6 pb-6 flex flex-wrap gap-3">
      <div class="chip">
        <Thermometer size="16" />
        <div class="chip-text">
          <span class="label">Temp</span>
          <span class="value">{sensor.temperature}</span>
        </div>
      </div>

      <div class="chip">
        <Droplets size="16" />
        <div class="chip-text">
          <span class="label">Humidity</span>
          <span class="value">{sensor.humidity}</span>
        </div>
      </div>

      <div class="chip">
        <Sprout size="16" />
        <div class="chip-text">
          <span class="label">Soil</span>
          <span class="value">{sensor.soil_moisture}</span>
        </div>
      </div>
    </div>
  </div>
</a>

<style>
  .chip {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 14px;
    background: rgba(0, 0, 0, 0.04);
    min-width: 110px;
  }

  .chip-text {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }

  .label {
    font-size: 10px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .value {
    font-size: 13px;
    font-weight: 600;
    color: #222;
  }
</style>
