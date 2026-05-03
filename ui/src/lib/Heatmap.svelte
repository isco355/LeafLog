<script>
  import { onMount } from "svelte";

  let chartContainer;

  const { heatmap_data } = $props();

  const prettyDate = (dates) => {
    const converter = (d) => {
      const new_d = new Date(d);
      return isNaN(new_d) ? d : new_d;
    };
    dates = dates.map((date) => converter(date));
    if (dates.length == 0 || typeof dates[0] == "string") {
      return dates;
    }
    const new_dates = dates.map((date) => date.toLocaleDateString("en-US"));
    return new_dates;
  };
  onMount(async () => {
    const Highcharts = (await import("highcharts")).default;
    await import("highcharts/modules/heatmap");
    if (heatmap_data) {
      const { columns, data, index, attribute, range } = heatmap_data;

      const resort = data.map((week_row, y_index) =>
        week_row.map((day, x_index) => [x_index, y_index, day]),
      );

      const heatmap_arr = resort.flat();
      Highcharts.chart(chartContainer, {
        chart: { type: "heatmap" },

        title: {
          text: ` ${attribute} Heatmap`,
        },

        xAxis: {
          categories: columns,
        },

        yAxis: {
          categories: prettyDate(index),
        },

        colorAxis: {
          min: range.min_val ?? 0,
          max: range.max_val ?? 100,
          minColor: "#f0f9ff",
          maxColor: "#fa4b3e",
        },

        legend: {
          align: "right",
          layout: "vertical",
          verticalAlign: "middle",
        },

        series: [
          {
            name: "values",
            borderWidth: 2,
            data: heatmap_arr,
            dataLabels: {
              enabled: true,
            },
          },
        ],
      });
    }
  });
</script>

<div bind:this={chartContainer} style="height: 500px;width:800px"></div>
