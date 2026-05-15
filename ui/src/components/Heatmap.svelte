<script>
  import { onMount } from "svelte";
  import Highcharts from "highcharts";
  import Heatmap from "highcharts/modules/heatmap";

  Heatmap(Highcharts);

  let chartContainer;

  const days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];

  function renderHeatmap(data) {
    Highcharts.chart(chartContainer, {
      chart: {
        type: "heatmap",
      },

      title: {
        text: "Sensor Heatmap (Mon–Sun)",
      },

      xAxis: {
        categories: Array.from({ length: 24 }, (_, i) => `${i}:00`),
      },

      yAxis: {
        categories: days,
        title: null,
      },

      colorAxis: {
        min: 0,
        minColor: "#ffffff",
        maxColor: "#ff4d4d",
      },

      legend: {
        align: "right",
        layout: "vertical",
        verticalAlign: "middle",
      },

      series: [
        {
          name: "Sensor intensity",
          borderWidth: 1,

          // Example static data
          data: data,

          dataLabels: {
            enabled: true,
            color: "#000",
          },
        },
      ],
    });
  }

  onMount(() => {
    // Example dataset (hour, dayIndex, value)
    const sampleData = [
      [0, 0, 5],
      [1, 0, 10],
      [2, 0, 7], // Monday
      [0, 1, 8],
      [1, 1, 12],
      [2, 1, 6], // Tuesday
      [0, 2, 4],
      [1, 2, 9],
      [2, 2, 11], // Wednesday
      [0, 3, 6],
      [1, 3, 8],
      [2, 3, 10], // Thursday
      [0, 4, 7],
      [1, 4, 13],
      [2, 4, 5], // Friday
      [0, 5, 3],
      [1, 5, 6],
      [2, 5, 9], // Saturday
      [0, 6, 2],
      [1, 6, 4],
      [2, 6, 8], // Sunday
    ];

    renderHeatmap(sampleData);
  });
</script>

<h1>heat map</h1>
<div bind:this={chartContainer} style="height: 500px;"></div>
