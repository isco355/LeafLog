<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { simulateSensorRequest } from "$lib/network";

  let count = $state(0);
  const createSimulateData = async () => {
    // count += 1;
    console.log("relog");
    await simulateSensorRequest().then((res) => {
      console.log(res);
      window.location.reload();
    });
  };

  onMount(() => {
    console.log("init");
  });
</script>

<h1>Simulate data</h1>

<button class="bg-white" onclick={createSimulateData}> Simulate </button>
