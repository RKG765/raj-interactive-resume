<script lang="ts">
	import { onMount } from "svelte";

	interface Commit {
		repo: string;
		message: string;
		sha: string;
		date: string;
	}

	// GitHub username — change this to your own
	const GITHUB_USERNAME = "RKG765";

	let commits = $state<Commit[]>([]);
	let loading = $state(true);
	let error = $state(false);

	onMount(async () => {
		try {
			// Fetch recent public events from GitHub API (no auth needed)
			const res = await fetch(
				`https://api.github.com/users/${GITHUB_USERNAME}/events/public?per_page=30`,
				{ headers: { Accept: "application/vnd.github.v3+json" } },
			);
			if (res.ok) {
				const events = await res.json();
				// Extract push events and their commits
				const pushEvents = events.filter(
					(e: any) => e.type === "PushEvent",
				);
				const extracted: Commit[] = [];

				for (const event of pushEvents) {
					const repo = event.repo?.name || "unknown";
					for (const c of event.payload?.commits || []) {
						extracted.push({
							repo,
							message: c.message.split("\n")[0], // first line only
							sha: c.sha?.substring(0, 7) || "",
							date: event.created_at || "",
						});
					}
				}

				// Deduplicate by sha and take latest 10
				const seen = new Set<string>();
				commits = extracted
					.filter((c) => {
						if (seen.has(c.sha)) return false;
						seen.add(c.sha);
						return true;
					})
					.slice(0, 10);
			} else {
				error = true;
			}
		} catch {
			error = true;
		} finally {
			loading = false;
		}
	});

	// Duplicate for seamless ticker scroll
	let displayCommits = $derived(
		commits.length > 0 ? [...commits, ...commits] : [],
	);
</script>

<div
	class="relative overflow-hidden border-b border-cyber-border/30 bg-cyber-surface/50 backdrop-blur-sm"
>
	<div class="flex items-center gap-3 px-4 py-2">
		<!-- Icon -->
		<div class="flex shrink-0 items-center gap-2">
			<div
				class="h-2 w-2 rounded-full bg-cyber-green animate-pulse"
			></div>
			<span
				class="text-[10px] font-semibold uppercase tracking-[0.2em] text-cyber-green/70"
			>
				Learning Tracker
			</span>
		</div>

		<!-- Divider -->
		<div class="h-4 w-px bg-cyber-border/50"></div>

		<!-- Ticker -->
		<div class="relative flex-1 overflow-hidden">
			{#if loading}
				<div class="flex items-center gap-2 text-xs text-cyber-text/50">
					<div
						class="h-3 w-3 animate-spin rounded-full border border-cyber-green/30 border-t-cyber-green"
					></div>
					<span>Fetching commits...</span>
				</div>
			{:else if error || commits.length === 0}
				<div class="flex items-center gap-2 text-xs text-cyber-text/40">
					<span
						>⦿ No recent commits found — push some code to see them
						here!</span
					>
				</div>
			{:else}
				<div
					class="ticker-scroll flex items-center gap-6 whitespace-nowrap"
				>
					{#each displayCommits as commit, i}
						<a
							href="https://github.com/{commit.repo}/commit/{commit.sha}"
							target="_blank"
							rel="noopener noreferrer"
							class="inline-flex items-center gap-2 text-xs hover:opacity-80 transition-opacity"
						>
							<span class="text-cyber-green/60">⦿</span>
							<span class="font-medium text-cyber-amber/80"
								>{commit.repo.split("/").pop()}</span
							>
							<span class="text-cyber-text/60">—</span>
							<span class="text-cyber-text/70"
								>{commit.message}</span
							>
							{#if commit.sha}
								<code
									class="rounded bg-cyber-border/30 px-1.5 py-0.5 text-[10px] text-cyber-green/50"
									>{commit.sha}</code
								>
							{/if}
						</a>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>
