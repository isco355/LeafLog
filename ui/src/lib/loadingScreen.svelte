<script>
  import { Sprout, Leaf, Flower2 } from "lucide-svelte";
  import { onMount } from "svelte";

  const stages = [
    { icon: Sprout, label: "Planting seeds..." },
    { icon: Leaf, label: "Growing roots..." },
    { icon: Flower2, label: "Blooming soon..." },
  ];

  let index = 0;
  let visible = true;

  function nextStage() {
    visible = false;

    setTimeout(() => {
      index = (index + 1) % stages.length;
      visible = true;
    }, 250);
  }

  onMount(() => {
    const interval = setInterval(nextStage, 1800);
    return () => clearInterval(interval);
  });
</script>

<div
  class="relative min-h-screen flex items-center justify-center bg-white text-black overflow-hidden"
>
  <div class="absolute inset-0 pointer-events-none">
    <div class="dot d1"></div>
    <div class="dot d2"></div>
    <div class="dot d3"></div>
  </div>

  <div class="flex flex-col items-center space-y-6 z-10">
    <div class="p-8 rounded-full border border-black/10 bg-white shadow-sm">
      {#if visible}
        <svelte:component
          this={stages[index].icon}
          class="w-20 h-20 text-black icon-grow"
        />
      {/if}
    </div>

    <div
      class="text-center transition-opacity duration-300 {visible
        ? 'opacity-100'
        : 'opacity-0'}"
    >
      <h1 class="text-lg font-medium tracking-wide">
        {stages[index].label}
      </h1>
    </div>

    <div class="w-56 h-[2px] bg-black/10 overflow-hidden rounded-full">
      <div class="progress"></div>
    </div>
  </div>
</div>

<style>
  .icon-grow {
    animation: grow 0.5s ease-out;
  }

  @keyframes grow {
    0% {
      transform: scale(0.4);
      opacity: 0;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .progress {
    height: 100%;
    width: 0%;
    background: black;
    animation: load 1.8s infinite ease-in-out;
  }

  @keyframes load {
    0% {
      width: 0%;
    }
    50% {
      width: 90%;
    }
    100% {
      width: 0%;
    }
  }

  .dot {
    position: absolute;
    width: 6px;
    height: 6px;
    background: black;
    opacity: 0.08;
    border-radius: 999px;
    animation: float 10s infinite linear;
  }

  .d1 {
    left: 20%;
    top: 90%;
    animation-duration: 12s;
  }
  .d2 {
    left: 60%;
    top: 95%;
    animation-duration: 9s;
  }
  .d3 {
    left: 80%;
    top: 85%;
    animation-duration: 11s;
  }

  @keyframes float {
    0% {
      transform: translateY(0);
      opacity: 0;
    }
    20% {
      opacity: 0.2;
    }
    100% {
      transform: translateY(-120vh);
      opacity: 0;
    }
  }
</style>
