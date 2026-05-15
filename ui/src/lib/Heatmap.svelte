<script>
  import { onMount } from "svelte";
  import { Droplets, Waves, Thermometer, Battery, Wifi } from "lucide-svelte";

  let chartContainer;
  const { heatmap_data } = $props();

  const iconMap = {
    soil_moisture: Droplets,
    humidity: Waves,
    temperature: Thermometer,
    battery: Battery,
    linkquality: Wifi,
  };

  const prettyDate = (dates) => {
    const converter = (d) => {
      const new_d = new Date(d);
      return isNaN(new_d) ? d : new_d;
    };

    dates = dates.map((date) => converter(date));

    if (dates.length == 0 || typeof dates[0] == "string") {
      return dates;
    }

    return dates.map((date) => date.toLocaleDateString("en-US"));
  };

  onMount(async () => {
    const Highcharts = (await import("highcharts")).default;
    await import("highcharts/modules/heatmap");

    if (!heatmap_data) return;

    const { columns, data, index, range } = heatmap_data;

    const resort = data.map((week_row, y_index) =>
      week_row.map((day, x_index) => [x_index, y_index, day]),
    );

    const heatmap_arr = resort.flat();

    Highcharts.chart(chartContainer, {
      chart: {
        type: "heatmap",
        backgroundColor: "#ffffff",
      },

      title: {
        text: null,
      },

      xAxis: {
        categories: columns,
        lineColor: "#e5e7eb",
        labels: {
          style: { color: "#374151" },
        },
      },

      yAxis: {
        categories: prettyDate(index),
        title: null,
        gridLineColor: "#f3f4f6",
        labels: {
          style: { color: "#374151" },
        },
      },

      colorAxis: {
        min: range.min_val ?? 0,
        max: range.max_val ?? 100,
        minColor: "#f8fafc",
        maxColor: "#eb0023",
      },

      legend: {
        align: "right",
        layout: "vertical",
        verticalAlign: "middle",
        itemStyle: {
          color: "#374151",
        },
      },

      series: [
        {
          name: "values",
          borderWidth: 1,
          borderColor: "#ffffff",
          data: heatmap_arr,
          dataLabels: {
            enabled: true,
            style: {
              color: "#111827",
              textOutline: "none",
            },
          },
        },
      ],

      credits: {
        enabled: false,
      },
    });
  });
</script>

<div class="space-y-2">
  <div
    class="flex items-center justify-center gap-2 text-zinc-900 font-medium w-full"
  >
    {#if iconMap[heatmap_data.attribute]}
      {@const Icon = iconMap[heatmap_data.attribute]}
      <Icon size={18} />
    {/if}
    <h1 class="text-lg">
      {heatmap_data.attribute}
    </h1>
  </div>

  <div
    bind:this={chartContainer}
    style="height: 500px; width: 800px;"
    class="bg-white"
  />
</div>
