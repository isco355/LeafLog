<script>
  import { onMount } from "svelte";
  import Highcharts from "highcharts";

  let chartContainer;
  let { series } = $props();

  function renderChart(seriesData) {
    Highcharts.chart(chartContainer, {
      line: {
        dataLabels: {
          enabled: true,
        },
      },
      chart: {
        type: "scatter",
      },
      title: {
        text: `Sensor  readings`,
      },
      xAxis: {
        type: "datetime",
      },
      yAxis: {
        title: { text: "Value" },
      },
      series: seriesData,
      exporting: {
        showTable: true,
      },
    });
  }

  onMount(async () => {
    // console.log(series);
    if (series) {
      renderChart(series);
    }
  });
</script>

<div bind:this={chartContainer} style="height: 400px;width:900px"></div>
