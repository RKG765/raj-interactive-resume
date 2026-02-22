<script lang="ts">
	import {
		getMode,
		getTheme,
		isTransitioning,
		toggleMode,
	} from "$lib/state.svelte";
	import GitHubTracker from "$lib/components/GitHubTracker.svelte";
	import Terminal from "$lib/components/Terminal.svelte";
	import "../app.css";

	let currentMode = $derived(getMode());
	let currentTheme = $derived(getTheme());
	let isTransition = $derived(isTransitioning());

	// Apply theme class to <html> reactively
	$effect(() => {
		const html = document.documentElement;
		html.classList.remove("dark", "light");
		html.classList.add(currentTheme);
	});

	let SceneComponent: any = $state(null);

	// Lazy-load Scene component (it includes Three.js)
	$effect(() => {
		if (currentMode === "scene" && !SceneComponent) {
			import("$lib/components/Scene.svelte").then((m) => {
				SceneComponent = m.default;
			});
		}
	});
</script>

<div class="flex h-screen flex-col overflow-hidden">
	<!-- GitHub Learning Tracker (persistent) -->
	<GitHubTracker />

	<!-- Mode Toggle Header -->
	<div
		class="flex items-center justify-between border-b px-4 py-2
		{currentTheme === 'dark'
			? 'border-cyber-border/30 bg-cyber-surface/60'
			: 'border-gray-200 bg-white/80 backdrop-blur-sm'}"
	>
		<div class="flex items-center gap-3">
			<h1
				class="text-sm font-bold tracking-wider
				{currentTheme === 'dark'
					? 'text-cyber-green'
					: 'bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'}"
			>
				RAJ KUMAR
			</h1>
			<span
				class="text-xs {currentTheme === 'dark'
					? 'text-cyber-text/40'
					: 'text-gray-400'}"
			>
				{currentMode === "terminal" ? "// terminal" : "// 3d explorer"}
			</span>
		</div>

		<button
			onclick={toggleMode}
			disabled={isTransition}
			class="group relative overflow-hidden rounded-lg px-4 py-2 text-xs font-semibold uppercase tracking-widest transition-all duration-300
				{currentTheme === 'dark'
				? 'border border-cyber-green/30 text-cyber-green hover:border-cyber-green/60 hover:bg-cyber-green/10 hover:shadow-[0_0_15px_rgba(0,255,65,0.15)]'
				: 'border border-indigo-300 text-indigo-600 hover:border-indigo-500 hover:bg-indigo-50 hover:shadow-lg'}
				{isTransition ? 'opacity-50' : ''}
			"
		>
			<span class="relative z-10">
				{currentMode === "terminal" ? "◐ Enter 3D" : "◑ Terminal"}
			</span>
		</button>
	</div>

	<!-- Main Content Area -->
	<div class="relative flex-1 overflow-hidden">
		<!-- Transition Overlay -->
		{#if isTransition}
			<div
				class="absolute inset-0 z-50 flex items-center justify-center
				{currentTheme === 'dark' ? 'bg-cyber-bg' : 'bg-white'}"
			>
				<div class="text-center">
					<div
						class="mb-4 h-8 w-8 animate-spin rounded-full border-2
						{currentTheme === 'dark'
							? 'border-cyber-green/20 border-t-cyber-green'
							: 'border-indigo-200 border-t-indigo-500'}"
					></div>
					<span
						class="text-xs uppercase tracking-widest
						{currentTheme === 'dark' ? 'text-cyber-green/60' : 'text-indigo-400'}"
					>
						{currentMode === "terminal"
							? "Loading 3D..."
							: "Booting terminal..."}
					</span>
				</div>
			</div>
		{/if}

		<!-- Terminal View -->
		{#if currentMode === "terminal"}
			<div class="h-full" class:opacity-0={isTransition}>
				<Terminal />
			</div>
		{:else}
			<!-- Scene View (lazy loaded) -->
			<div class="h-full" class:opacity-0={isTransition}>
				{#if SceneComponent}
					<svelte:component this={SceneComponent} />
				{:else}
					<div
						class="flex h-full items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-purple-50"
					>
						<div class="text-center">
							<div
								class="mb-4 h-8 w-8 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-500 mx-auto"
							></div>
							<span
								class="text-xs text-indigo-400 uppercase tracking-widest"
								>Loading 3D scene...</span
							>
						</div>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
