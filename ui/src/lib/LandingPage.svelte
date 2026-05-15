<script>
  import { Leaf } from "lucide-svelte";
</script>

<div
  class="min-h-screen bg-white text-zinc-900 flex items-center justify-center px-6"
>
  <div class="text-center space-y-6">
    <div class="relative flex items-center justify-center w-56 h-56 mx-auto">
      <div
        class="absolute w-32 h-32 rounded-full bg-zinc-100 animate-pulse"
      ></div>

      <div
        class="absolute w-48 h-48 rounded-full border border-zinc-200 animate-[ping_4s_ease-in-out_infinite] opacity-40"
      ></div>

      <div class="relative z-10 animate-float">
        <Leaf class="w-20 h-20 text-zinc-700" />
      </div>
    </div>

    <h1 class="text-4xl font-bold tracking-tight">
      Living plant monitoring system
    </h1>

    <p class="text-zinc-600 max-w-md mx-auto">
      Real-time insights into soil moisture, temperature, humidity, and plant
      health.
    </p>

    <div class="flex items-center justify-center gap-3 pt-2">
      <a
        href="/dashboard"
        class="px-5 py-2 bg-zinc-900 text-white rounded-lg text-sm hover:bg-zinc-800 transition"
      >
        Dashboard
      </a>

      <a
        href="/developers"
        class="px-5 py-2 border border-zinc-300 rounded-lg text-sm hover:bg-zinc-50 transition"
      >
        Developers
      </a>
    </div>
  </div>
</div>

<style>
  .animate-float {
    animation: float 3.5s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-8px);
    }
  }
</style>
