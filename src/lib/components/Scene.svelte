<script lang="ts">
    import { Canvas } from "@threlte/core";
    import { onMount } from "svelte";
    import SceneContent from "./SceneContent.svelte";

    let mounted = $state(false);
    let searchQuery = $state("");
    let searchResults = $state<string[]>([]);
    let showSearch = $state(false);
    let selectedInfo = $state<{ title: string; content: string } | null>(null);

    onMount(() => {
        mounted = true;
    });

    function handleSearch() {
        const q = searchQuery.toLowerCase();
        const data: Record<string, string[]> = {
            python: [
                "PyGit Version Control System",
                "Job Scraper (FastAPI + Scrapy)",
                "AI Gateway Backend",
            ],
            devops: [
                "SWAN Livelihood Internship",
                "CI/CD Pipeline Architecture",
                "Nginx & Cloud Deployments",
            ],
            ai: [
                "Secure AI Gateway",
                "AI Email Agent",
                "Groq LLaMA Integration",
            ],
            dsa: [
                "Graph Theory & BFS/DFS",
                "Dynamic Programming",
                "Binary Trees & Heaps",
            ],
            backend: [
                "FastAPI Microservices",
                "PostgreSQL + Redis",
                "Celery Task Queues",
            ],
            design: [
                "LLD & SOLID Principles",
                "Design Patterns (C++)",
                "System Design Case Studies",
            ],
        };

        searchResults = [];
        for (const [key, values] of Object.entries(data)) {
            if (
                key.includes(q) ||
                values.some((v) => v.toLowerCase().includes(q))
            ) {
                searchResults = [
                    ...searchResults,
                    ...values.filter(
                        (v) => v.toLowerCase().includes(q) || key.includes(q),
                    ),
                ];
            }
        }
        if (searchResults.length === 0 && q.length > 0) {
            searchResults = ["No results found. Try: python, devops, ai, dsa"];
        }
    }

    function closeInfo() {
        selectedInfo = null;
    }

    function handleNodeClick(detail: { title: string; content: string }) {
        selectedInfo = detail;
    }
</script>

<div
    class="relative h-full w-full overflow-hidden bg-gradient-to-br from-indigo-50 via-white to-purple-50"
>
    <!-- 3D Canvas -->
    {#if mounted}
        <div class="absolute inset-0">
            <Canvas>
                <SceneContent onNodeClick={handleNodeClick} />
            </Canvas>
        </div>
    {/if}

    <!-- Floating Search Bar -->
    <div class="absolute left-1/2 top-6 z-20 -translate-x-1/2">
        <div class="group relative">
            <div
                class="absolute -inset-1 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-50 blur-lg transition-opacity group-hover:opacity-75"
            ></div>
            <div
                class="relative flex items-center gap-3 rounded-2xl border border-white/30 bg-white/90 px-5 py-3 shadow-2xl backdrop-blur-xl"
            >
                <svg
                    class="h-5 w-5 text-indigo-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                </svg>
                <input
                    bind:value={searchQuery}
                    oninput={handleSearch}
                    onfocus={() => (showSearch = true)}
                    type="text"
                    placeholder="Search portfolio... (python, devops, ai, dsa)"
                    class="w-64 border-none bg-transparent text-sm text-gray-800 outline-none placeholder:text-gray-400 md:w-96"
                />
                {#if searchQuery}
                    <button
                        onclick={() => {
                            searchQuery = "";
                            searchResults = [];
                        }}
                        class="text-gray-400 transition-colors hover:text-gray-600"
                    >
                        ✕
                    </button>
                {/if}
            </div>

            <!-- Search Results Dropdown -->
            {#if showSearch && searchResults.length > 0}
                <div
                    class="absolute left-0 right-0 top-full mt-2 overflow-hidden rounded-xl border border-white/30 bg-white/95 shadow-2xl backdrop-blur-xl"
                >
                    {#each searchResults as result, i}
                        <button
                            onclick={() => {
                                showSearch = false;
                                selectedInfo = {
                                    title: result,
                                    content: `Explore more about ${result} in the 3D scene below.`,
                                };
                            }}
                            class="flex w-full items-center gap-3 px-4 py-3 text-left text-sm text-gray-700 transition-colors hover:bg-indigo-50"
                        >
                            <span
                                class="flex h-6 w-6 items-center justify-center rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-[10px] font-bold text-white"
                            >
                                {i + 1}
                            </span>
                            {result}
                        </button>
                    {/each}
                </div>
            {/if}
        </div>
    </div>

    <!-- Info Panel (click a 3D node) -->
    {#if selectedInfo}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
            class="absolute inset-0 z-30 flex items-center justify-center bg-black/30 backdrop-blur-sm"
            onclick={closeInfo}
        >
            <div
                class="animate-[fade-up_0.3s_ease-out] mx-4 max-h-[80vh] w-full max-w-lg overflow-y-auto rounded-2xl border border-white/30 bg-white/95 p-8 shadow-2xl backdrop-blur-xl"
                onclick={(e) => e.stopPropagation()}
            >
                <div class="mb-4 flex items-center justify-between">
                    <h2
                        class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-xl font-bold text-transparent"
                    >
                        {selectedInfo.title}
                    </h2>
                    <button
                        onclick={closeInfo}
                        class="rounded-full p-2 text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
                    >
                        ✕
                    </button>
                </div>
                <div
                    class="whitespace-pre-wrap font-['Inter'] text-sm leading-relaxed text-gray-600"
                >
                    {selectedInfo.content}
                </div>
            </div>
        </div>
    {/if}

    <!-- Labels Overlay -->
    <div class="pointer-events-none absolute bottom-8 left-8 z-10">
        <div class="space-y-2">
            <div class="flex items-center gap-2">
                <div class="h-3 w-3 rounded-full bg-indigo-500"></div>
                <span class="text-xs font-medium text-gray-500"
                    >DSA Graph Nodes — Click to Explore</span
                >
            </div>
            <div class="flex items-center gap-2">
                <div class="h-3 w-3 rounded-full bg-emerald-500"></div>
                <span class="text-xs font-medium text-gray-500"
                    >DevOps Server Rack — Click Blades</span
                >
            </div>
        </div>
    </div>
</div>
