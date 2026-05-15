<script>
  import { onMount } from "svelte";

  let chartContainer;

  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  function getWeekLabels(count) {
    return Array.from({ length: count }, (_, i) => `Week ${i + 1}`);
  }

  onMount(async () => {
    const Highcharts = (await import("highcharts")).default;
    await import("highcharts/modules/heatmap");

    // Example: 4 weeks
    const weeks = 4;

    const sampleData = [
      [0, 0, 5],
      [1, 0, 8],
      [2, 0, 6],
      [3, 0, 7],
      [4, 0, 9],
      [5, 0, 4],
      [6, 0, 3],
      [0, 1, 7],
      [1, 1, 6],
      [2, 1, 5],
      [3, 1, 8],
      [4, 1, 10],
      [5, 1, 6],
      [6, 1, 9],
      [0, 2, 4],
      [1, 2, 3],
      [2, 2, 6],
      [3, 2, 7],
      [4, 2, 8],
      [5, 2, 5],
      [6, 2, 6],
      [0, 3, 9],
      [1, 3, 7],
      [2, 3, 8],
      [3, 3, 6],
      [4, 3, 5],
      [5, 3, 4],
      [6, 3, 7],
    ];

    Highcharts.chart(chartContainer, {
      chart: { type: "heatmap" },

      title: {
        text: "Weekly Sensor Heatmap",
      },

      xAxis: {
        categories: days,
        title: { text: "Day of Week" },
      },

      yAxis: {
        categories: getWeekLabels(weeks),
        title: { text: "Weeks" },
        reversed: true, // optional: newest week on top
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
          borderWidth: 1,
          data: sampleData,
          dataLabels: {
            enabled: true,
          },
        },
      ],
    });
  });
</script>

<div bind:this={chartContainer} style="height: 500px;width:800px"></div>
