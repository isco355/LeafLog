<script>
  const { record } = $props();

  const {
    device_name,
    battery,
    humidity,
    temperature,
    soil_moisture,
    linkquality,
    dry,
    ts,
  } = record;

  const formatDate = (ts) => {
    const dateObj = new Date(ts);

    return `${dateObj.toLocaleDateString("en-GB", {
      weekday: "short",
      day: "2-digit",
      month: "2-digit",
    })} ${dateObj.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    })}`;
  };
</script>

<div
  class="w-full flex flex-col md:flex-row md:items-center justify-between gap-4 rounded-2xl border border-gray-200 bg-white shadow-sm p-4"
>
  <div class="flex flex-col min-w-[180px]">
    <p class="text-xs text-gray-500">
      {formatDate(ts)}
    </p>
  </div>

  <div class="flex flex-wrap items-center gap-4 text-sm">
    <div class="flex flex-col">
      <span class="text-xs text-gray-500">Battery</span>
      <span class="font-semibold text-gray-900">{battery}%</span>
    </div>

    <div class="flex flex-col">
      <span class="text-xs text-gray-500">Humidity</span>
      <span class="font-semibold text-gray-900">{humidity}%</span>
    </div>

    <div class="flex flex-col">
      <span class="text-xs text-gray-500">Temp</span>
      <span class="font-semibold text-gray-900">{temperature}°C</span>
    </div>

    <div class="flex flex-col">
      <span class="text-xs text-gray-500">Soil</span>
      <span class="font-semibold text-gray-900">{soil_moisture}%</span>
    </div>

    <div class="flex flex-col">
      <span class="text-xs text-gray-500">Link</span>
      <span class="font-semibold text-gray-900">{linkquality}</span>
    </div>
  </div>

  <!-- Right: Status -->
  <div class="flex items-center gap-2">
    <span class="text-xs text-gray-500">Dry:</span>

    <span
      class={`px-2 py-1 rounded-full text-xs font-medium ${
        dry ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
      }`}
    >
      {dry ? "Dry" : "OK"}
    </span>
  </div>
</div>
