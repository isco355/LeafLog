<script>
  import { onMount, tick } from "svelte";
  import Highcharts from "highcharts";
  import {
    LineChart,
    BarChart2,
    AreaChart,
    Waves,
    ChartScatter,
  } from "lucide-svelte";

  const options = [
    // { value: "line", icon: LineChart, label: "Line" },
    { value: "spline", icon: Waves, label: "Spline" },
    { value: "column", icon: BarChart2, label: "Column" },
    { value: "area", icon: AreaChart, label: "Area" },
    { value: "scatter", icon: ChartScatter, label: "scatter" },
  ];

  let chartContainer;
  let chart;

  let chartType = $state("spline");
  let { series } = $props();

  function createChart() {
    if (!series) return;

    chart?.destroy();

    chart = Highcharts.chart(chartContainer, {
      chart: { type: chartType },
      title: { text: "Sensor readings" },
      xAxis: { type: "datetime" },
      yAxis: { title: { text: "Value" } },
      series: series,
      exporting: { showTable: true },
    });
  }

  $effect(() => {
    if (!series) return;
    createChart();
  });

  onMount(async () => {
    await tick();
    createChart();
  });

  function updateChart() {
    createChart();
  }
</script>

<div
  class="flex items-center gap-1 rounded-xl border border-zinc-200 bg-white p-1 w-fit shadow-sm"
>
  {#each options as opt}
    <button
      type="button"
      on:click={() => {
        chartType = opt.value;
        updateChart();
      }}
      class="
        flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all
        {chartType === opt.value
        ? 'bg-black text-white'
        : 'text-zinc-600 hover:text-black hover:bg-zinc-100'}
      "
    >
      <opt.icon size={16} />
      <span class="hidden sm:inline">{opt.label}</span>
    </button>
  {/each}
</div>

<div class="flex gap-2 items-center my-3"></div>

<div bind:this={chartContainer} style="height: 400px;"></div>
