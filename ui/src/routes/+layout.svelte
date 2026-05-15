<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";

	import { LayoutDashboard } from "lucide-svelte";
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<!-- <script> -->
<!-- </script> -->

<nav
	class="flex items-center justify-between border-b border-zinc-200 bg-white px-6 py-4"
>
	<h1 class="text-xl font-semibold text-black">LeafLog</h1>

	<a
		href="/dashboard"
		class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-4 py-2 text-sm font-medium text-black transition hover:bg-zinc-100"
	>
		<LayoutDashboard class="h-4 w-4" />
		Dashboard
	</a>
</nav>
{@render children()}
