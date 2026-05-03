<script>
  import { onMount } from "svelte";

  let chartContainer;

  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  function getWeekLabels(count) {
    return Array.from({ length: count }, (_, i) => `Week ${i + 1}`);
  }

  onMount(async () => {
    const Highcharts = (await import("highcharts")).default;

    await import("highcharts/modules/tilemap");

    const weeks = 4;

    // convert heatmap-style grid → tilemap format
    const sampleData = [
      { x: 0, y: 0, value: 5 },
      { x: 1, y: 0, value: 8 },
      { x: 2, y: 0, value: 6 },
      { x: 3, y: 0, value: 7 },
      { x: 4, y: 0, value: 9 },
      { x: 5, y: 0, value: 4 },
      { x: 6, y: 0, value: 3 },

      { x: 0, y: 1, value: 7 },
      { x: 1, y: 1, value: 6 },
      { x: 2, y: 1, value: 5 },
      { x: 3, y: 1, value: 8 },
      { x: 4, y: 1, value: 10 },
      { x: 5, y: 1, value: 6 },
      { x: 6, y: 1, value: 9 },

      { x: 0, y: 2, value: 4 },
      { x: 1, y: 2, value: 3 },
      { x: 2, y: 2, value: 6 },
      { x: 3, y: 2, value: 7 },
      { x: 4, y: 2, value: 8 },
      { x: 5, y: 2, value: 5 },
      { x: 6, y: 2, value: 6 },

      { x: 0, y: 3, value: 9 },
      { x: 1, y: 3, value: 7 },
      { x: 2, y: 3, value: 8 },
      { x: 3, y: 3, value: 6 },
      { x: 4, y: 3, value: 5 },
      { x: 5, y: 3, value: 4 },
      { x: 6, y: 3, value: 7 },
    ];

    Highcharts.chart(chartContainer, {
      chart: {
        type: "tilemap",
      },

      title: {
        text: "Weekly Sensor Honeycomb Heatmap",
      },

      xAxis: {
        categories: days,
        title: { text: "Day of Week" },
      },

      yAxis: {
        categories: getWeekLabels(weeks),
        reversed: true,
        title: { text: "Weeks" },
      },

      colorAxis: {
        min: 0,
        minColor: "#f0f9ff",
        maxColor: "#0369a1",
      },

      legend: {
        align: "right",
        layout: "vertical",
        verticalAlign: "middle",
      },

      series: [
        {
          name: "Sensor value",
          data: sampleData,
          tileShape: "hexagon", // 🐝 honeycomb mode
          borderWidth: 1,
          dataLabels: {
            enabled: true,
            format: "{point.value}",
          },
        },
      ],
    });
  });
</script>

<div bind:this={chartContainer} style="height: 400px;"></div>
