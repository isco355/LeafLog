<script>
  import { RefreshCw, Home } from "lucide-svelte";
  let retrying = false;

  function retry() {
    retrying = true;
    setTimeout(() => {
      retrying = false;
      window.location.reload();
    }, 1600);
  }
</script>

<div
  class="min-h-screen flex items-center justify-center bg-[#f6f6f4] relative overflow-hidden text-stone-900"
>
  <!-- Ambient background glow -->
  <div
    class="absolute w-[600px] h-[600px] bg-emerald-200/30 blur-[140px] rounded-full -top-40 -left-40"
  ></div>
  <div
    class="absolute w-[500px] h-[500px] bg-stone-300/40 blur-[140px] rounded-full -bottom-40 -right-40"
  ></div>

  <!-- Glass container -->
  <div
    class="relative z-10 w-full max-w-md mx-6 rounded-3xl bg-white/60 backdrop-blur-xl border border-white/40 shadow-xl p-10 text-center"
  >
    <!-- Title -->
    <h1 class="text-2xl font-serif tracking-tight mb-2">System Offline</h1>

    <p class="text-sm text-stone-500 mb-10 leading-relaxed">
      The data ecosystem has temporarily dried out. Rehydration may restore
      connection.
    </p>

    <!-- Core visualization -->
    <div
      class="relative w-40 h-40 mx-auto mb-10 flex items-center justify-center"
    >
      <!-- Outer pulse ring -->
      <div
        class={`absolute inset-0 rounded-full transition-all duration-1000
        ${retrying ? "bg-emerald-200/60 scale-110 animate-pulse" : "bg-stone-200/40 scale-100"}`}
      ></div>

      <!-- Inner core -->
      <div
        class={`relative w-24 h-24 rounded-full flex items-center justify-center transition-all duration-700
        ${retrying ? "bg-emerald-500 shadow-lg shadow-emerald-200" : "bg-stone-400"}`}
      >
        <!-- Icon-like plant mark -->
        <div
          class={`w-10 h-10 rounded-full transition-all duration-700
          ${retrying ? "bg-white scale-110" : "bg-stone-200 scale-90"}`}
        ></div>
      </div>

      <!-- floating particles -->
      <div
        class={`absolute inset-0 transition-opacity duration-700 ${retrying ? "opacity-100" : "opacity-0"}`}
      >
        <div
          class="absolute w-2 h-2 bg-emerald-400 rounded-full top-6 left-10 animate-bounce"
        ></div>
        <div
          class="absolute w-1.5 h-1.5 bg-emerald-300 rounded-full bottom-8 right-10 animate-bounce"
        ></div>
        <div
          class="absolute w-1 h-1 bg-emerald-500 rounded-full top-10 right-12 animate-bounce"
        ></div>
      </div>
    </div>

    <!-- Action -->
    <div class="flex flex-col gap-3">
      <button
        on:click={retry}
        disabled={retrying}
        class="relative overflow-hidden rounded-full px-6 py-3 bg-stone-900 text-white font-medium transition active:scale-95 disabled:opacity-60"
      >
        <div class="flex items-center justify-center gap-2 relative z-10">
          <RefreshCw class={`w-4 h-4 ${retrying ? "animate-spin" : ""}`} />
          {retrying ? "Rehydrating..." : "Reconnect System"}
        </div>

        {#if retrying}
          <div class="absolute inset-0 bg-emerald-500 animate-pulse"></div>
        {/if}
      </button>

      <a
        href="/"
        class="flex items-center justify-center gap-2 text-sm text-stone-500 hover:text-stone-900 transition"
      >
        <Home class="w-4 h-4" />
        Return Home
      </a>
    </div>
  </div>
</div>
