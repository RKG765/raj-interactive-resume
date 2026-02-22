<script lang="ts">
	import { onMount } from 'svelte';

	interface Commit {
		repo: string;
		message: string;
		sha: string;
		date: string;
	}

	let commits = $state<Commit[]>([]);
	let loading = $state(true);
	let error = $state(false);

	onMount(async () => {
		try {
			const res = await fetch('/api/github');
			if (res.ok) {
				const data = await res.json();
				commits = data.commits || [];
			} else {
				error = true;
			}
		} catch {
			error = true;
		} finally {
			loading = false;
		}
	});

	let displayCommits = $derived(
		commits.length > 0 ? [...commits, ...commits] : []
	);
</script>

<div class="relative overflow-hidden border-b border-cyber-border/30 bg-cyber-surface/50 backdrop-blur-sm dark:border-cyber-border/30 dark:bg-cyber-surface/50">
	<div class="flex items-center gap-3 px-4 py-2">
		<!-- Icon -->
		<div class="flex shrink-0 items-center gap-2">
			<div class="h-2 w-2 rounded-full bg-cyber-green animate-pulse"></div>
			<span class="text-[10px] font-semibold uppercase tracking-[0.2em] text-cyber-green/70">
				Learning Tracker
			</span>
		</div>

		<!-- Divider -->
		<div class="h-4 w-px bg-cyber-border/50"></div>

		<!-- Ticker -->
		<div class="relative flex-1 overflow-hidden">
			{#if loading}
				<div class="flex items-center gap-2 text-xs text-cyber-text/50">
					<div class="h-3 w-3 animate-spin rounded-full border border-cyber-green/30 border-t-cyber-green"></div>
					<span>Fetching commits...</span>
				</div>
			{:else if error || commits.length === 0}
				<div class="flex items-center gap-4 text-xs text-cyber-text/40">
					<span>⦿ rajkumar/pygit — Implement three-way merge</span>
					<span>⦿ rajkumar/portfolio — Build terminal interface</span>
					<span>⦿ rajkumar/job-scraper — Add Redis caching</span>
				</div>
			{:else}
				<div class="ticker-scroll flex items-center gap-6 whitespace-nowrap">
					{#each displayCommits as commit, i}
						<span class="inline-flex items-center gap-2 text-xs">
							<span class="text-cyber-green/60">⦿</span>
							<span class="font-medium text-cyber-amber/80">{commit.repo.split('/').pop()}</span>
							<span class="text-cyber-text/60">—</span>
							<span class="text-cyber-text/70">{commit.message}</span>
							{#if commit.sha}
								<code class="rounded bg-cyber-border/30 px-1.5 py-0.5 text-[10px] text-cyber-green/50">{commit.sha}</code>
							{/if}
						</span>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>
