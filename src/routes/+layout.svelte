<script lang="ts">
	import Terminal from "$lib/components/Terminal.svelte";
	import "../app.css";

	// Set dark theme on mount
	$effect(() => {
		const html = document.documentElement;
		html.classList.remove("dark", "light");
		html.classList.add("dark");
	});
</script>

<div class="flex h-screen flex-col overflow-hidden">
	<!-- Header -->
	<div
		class="flex items-center justify-between border-b px-4 py-2
		border-cyber-border/30 bg-cyber-surface/60"
	>
		<h1 class="text-sm font-bold tracking-wider text-cyber-green">
			RAJ KUMAR
		</h1>
	</div>

	<!-- Terminal -->
	<div class="relative flex-1 overflow-hidden">
		<Terminal />
	</div>
</div>
