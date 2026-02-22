<script lang="ts">
    import { T, useTask } from "@threlte/core";
    import { OrbitControls, Text, interactivity } from "@threlte/extras";
    import * as THREE from "three";

    interactivity();

    type NodeClickHandler = (detail: {
        title: string;
        content: string;
    }) => void;

    let { onNodeClick }: { onNodeClick: NodeClickHandler } = $props();

    // ── DSA Graph Data ──────────────────────────────────
    const graphNodes = [
        {
            id: "bfs",
            label: "BFS",
            pos: [-4, 2, 0] as [number, number, number],
            color: "#6366f1",
            info: "Breadth-First Search\n\nTraverses a graph level by level using a queue.\nTime: O(V + E) | Space: O(V)\n\nUsed in:\n• Shortest path in unweighted graphs\n• Level-order tree traversal\n• Social network friend suggestions\n• Web crawlers (layer-by-layer discovery)",
        },
        {
            id: "dfs",
            label: "DFS",
            pos: [-2, 3.5, -1] as [number, number, number],
            color: "#8b5cf6",
            info: "Depth-First Search\n\nExplores as deep as possible before backtracking.\nTime: O(V + E) | Space: O(V)\n\nUsed in:\n• Topological sorting\n• Cycle detection\n• Maze generation/solving\n• Connected components",
        },
        {
            id: "dp",
            label: "DP",
            pos: [-5, 3.5, 1] as [number, number, number],
            color: "#a855f7",
            info: "Dynamic Programming\n\nOptimal substructure + overlapping subproblems.\n\nKey Patterns:\n• Memoization (top-down)\n• Tabulation (bottom-up)\n• State compression\n\nClassic Problems:\n• 0/1 Knapsack, LCS, LIS\n• Matrix chain multiplication\n• Edit distance",
        },
        {
            id: "dijkstra",
            label: "Dijkstra",
            pos: [-3, 0.5, 0.5] as [number, number, number],
            color: "#ec4899",
            info: "Dijkstra's Algorithm\n\nSingle-source shortest path (non-negative weights).\nTime: O((V+E) log V) with min-heap\n\nKey insight: Greedy selection of nearest\nunvisited vertex guarantees optimality.\n\nVariants: A* (with heuristic), Bellman-Ford (neg weights)",
        },
        {
            id: "graph",
            label: "Graph",
            pos: [-4.5, 1, -0.5] as [number, number, number],
            color: "#3b82f6",
            info: "Graph Theory Fundamentals\n\nRepresentations:\n• Adjacency Matrix: O(V²) space, O(1) lookup\n• Adjacency List: O(V+E) space, efficient iteration\n\nTypes: Directed, Undirected, Weighted, DAG\n\nKey concepts: Degree, Path, Cycle,\nConnected Components, Bipartite",
        },
        {
            id: "tree",
            label: "Trees",
            pos: [-2.5, 1.5, 1] as [number, number, number],
            color: "#14b8a6",
            info: "Tree Data Structures\n\n• Binary Trees → BST, AVL, Red-Black\n• Heaps → Min-heap, Max-heap, Priority Queue\n• Tries → Prefix trees for string operations\n• Segment Trees → Range queries in O(log n)\n• Fenwick Trees → BIT for prefix sums",
        },
    ];

    const graphEdges: [number, number][] = [
        [0, 1],
        [0, 4],
        [1, 2],
        [3, 4],
        [4, 5],
        [1, 5],
        [0, 3],
    ];

    // ── Server Rack Data ────────────────────────────────
    const serverBlades = [
        {
            y: -1.5,
            color: "#059669",
            label: "CI/CD",
            info: "CI/CD Pipeline @ SWAN Livelihood\n\nTech:\n• GitHub Actions for automated builds\n• Docker multi-stage builds\n• Automated test suites with coverage\n• Blue-green deployment strategy\n\nAchievement: Reduced deployment time by 60%",
        },
        {
            y: -0.5,
            color: "#0d9488",
            label: "Nginx",
            info: "Nginx Reverse Proxy\n\nResponsibilities:\n• Load balancing across app instances\n• SSL/TLS termination (Let's Encrypt)\n• Static file serving with caching\n• Rate limiting & request throttling\n• WebSocket proxying for real-time features",
        },
        {
            y: 0.5,
            color: "#0891b2",
            label: "Cloud",
            info: "Cloud Deployments\n\nExperience with:\n• AWS EC2 + S3 for compute & storage\n• Docker Compose for orchestration\n• Environment-based config management\n• Monitoring with Prometheus + Grafana\n• Log aggregation with ELK stack",
        },
        {
            y: 1.5,
            color: "#2563eb",
            label: "Docker",
            info: "Docker & Containerization\n\n• Multi-stage builds for minimal images\n• Docker Compose for dev environments\n• Container networking & volumes\n• Image optimization (< 100MB for Python apps)\n• Registry management & versioned tags",
        },
    ];

    // ── Animation state ─────────────────────────────────
    let time = $state(0);
    let hoveredNode = $state<string | null>(null);
    let animatingNode = $state<string | null>(null);

    useTask((delta) => {
        time += delta;
    });

    function getNodeScale(id: string): number {
        if (animatingNode === id) return 1.4;
        if (hoveredNode === id) return 1.2;
        return 1.0;
    }

    function handleGraphNodeClick(node: (typeof graphNodes)[0]) {
        animatingNode = node.id;
        setTimeout(() => {
            animatingNode = null;
        }, 600);
        onNodeClick({ title: node.label, content: node.info });
    }

    function handleBladeClick(blade: (typeof serverBlades)[0]) {
        onNodeClick({ title: `DevOps: ${blade.label}`, content: blade.info });
    }
</script>

<!-- Camera & Lighting -->
<T.PerspectiveCamera makeDefault position={[0, 2, 10]} fov={50}>
    <OrbitControls
        enableDamping
        dampingFactor={0.05}
        enablePan={false}
        minDistance={5}
        maxDistance={20}
        autoRotate
        autoRotateSpeed={0.3}
    />
</T.PerspectiveCamera>

<T.AmbientLight intensity={0.6} />
<T.DirectionalLight position={[5, 8, 5]} intensity={1.0} castShadow />
<T.PointLight position={[-5, 3, 0]} intensity={0.5} color="#6366f1" />
<T.PointLight position={[5, 3, 0]} intensity={0.5} color="#14b8a6" />

<!-- Grid ground -->
<T.GridHelper args={[30, 30, "#e2e8f0", "#f1f5f9"]} position.y={-3} />

<!-- ── DSA Graph (Left Side) ──────────────────────── -->
<T.Group position={[0, 0, 0]}>
    <!-- Edges -->
    {#each graphEdges as [from, to]}
        {@const a = graphNodes[from].pos}
        {@const b = graphNodes[to].pos}
        {@const midX = (a[0] + b[0]) / 2}
        {@const midY = (a[1] + b[1]) / 2}
        {@const midZ = (a[2] + b[2]) / 2}
        {@const dx = b[0] - a[0]}
        {@const dy = b[1] - a[1]}
        {@const dz = b[2] - a[2]}
        {@const length = Math.sqrt(dx * dx + dy * dy + dz * dz)}
        <T.Mesh position={[midX, midY, midZ]} lookAt={[b[0], b[1], b[2]]}>
            <T.CylinderGeometry args={[0.02, 0.02, length, 8]} />
            <T.MeshStandardMaterial color="#c7d2fe" transparent opacity={0.5} />
        </T.Mesh>
    {/each}

    <!-- Nodes -->
    {#each graphNodes as node}
        {@const s = getNodeScale(node.id)}
        {@const bobY =
            Math.sin(time * 0.8 + graphNodes.indexOf(node) * 1.2) * 0.15}
        <T.Group position={[node.pos[0], node.pos[1] + bobY, node.pos[2]]}>
            <!-- Sphere -->
            <T.Mesh
                scale={[s, s, s]}
                onclick={() => handleGraphNodeClick(node)}
                onpointerenter={() => {
                    hoveredNode = node.id;
                    document.body.style.cursor = "pointer";
                }}
                onpointerleave={() => {
                    hoveredNode = null;
                    document.body.style.cursor = "default";
                }}
            >
                <T.SphereGeometry args={[0.35, 32, 32]} />
                <T.MeshStandardMaterial
                    color={node.color}
                    emissive={node.color}
                    emissiveIntensity={hoveredNode === node.id ? 0.6 : 0.2}
                    roughness={0.3}
                    metalness={0.5}
                />
            </T.Mesh>
            <!-- Label below -->
            <Text
                text={node.label}
                fontSize={0.2}
                position={[0, -0.6, 0]}
                color="#64748b"
                anchorX="center"
                anchorY="middle"
                font="https://fonts.googleapis.com/css2?family=Inter:wght@600"
            />
        </T.Group>
    {/each}

    <!-- Section Title -->
    <Text
        text="DSA Graph Visualizer"
        fontSize={0.3}
        position={[-3.5, 5, 0]}
        color="#6366f1"
        anchorX="center"
        anchorY="middle"
        font="https://fonts.googleapis.com/css2?family=Inter:wght@700"
    />
</T.Group>

<!-- ── Server Rack (Right Side) ───────────────────── -->
<T.Group position={[5, 0, -1]}>
    <!-- Rack Frame -->
    <T.Mesh position={[0, 0, 0]}>
        <T.BoxGeometry args={[2.5, 5, 1.2]} />
        <T.MeshStandardMaterial
            color="#1e293b"
            transparent
            opacity={0.3}
            roughness={0.8}
        />
    </T.Mesh>

    <!-- Server Blades -->
    {#each serverBlades as blade, i}
        {@const isHovered = hoveredNode === `blade-${i}`}
        <T.Mesh
            position={[0, blade.y, 0.15]}
            scale={isHovered ? [1.02, 1.02, 1.02] : [1, 1, 1]}
            onclick={() => handleBladeClick(blade)}
            onpointerenter={() => {
                hoveredNode = `blade-${i}`;
                document.body.style.cursor = "pointer";
            }}
            onpointerleave={() => {
                hoveredNode = null;
                document.body.style.cursor = "default";
            }}
        >
            <T.BoxGeometry args={[2.2, 0.7, 0.8]} />
            <T.MeshStandardMaterial
                color={blade.color}
                emissive={blade.color}
                emissiveIntensity={isHovered ? 0.4 : 0.1}
                roughness={0.4}
                metalness={0.6}
            />
        </T.Mesh>

        <!-- Blade Label -->
        <Text
            text={blade.label}
            fontSize={0.18}
            position={[0, blade.y, 0.65]}
            color="white"
            anchorX="center"
            anchorY="middle"
        />

        <!-- LED indicators -->
        <T.Mesh position={[0.9, blade.y + 0.2, 0.61]}>
            <T.SphereGeometry args={[0.04, 16, 16]} />
            <T.MeshStandardMaterial
                color="#22c55e"
                emissive="#22c55e"
                emissiveIntensity={0.8 + Math.sin(time * 3 + i) * 0.3}
            />
        </T.Mesh>
    {/each}

    <!-- Rack Title -->
    <Text
        text="DevOps Server Rack"
        fontSize={0.25}
        position={[0, 3, 0]}
        color="#0d9488"
        anchorX="center"
        anchorY="middle"
        font="https://fonts.googleapis.com/css2?family=Inter:wght@700"
    />

    <Text
        text="SWAN Livelihood Internship"
        fontSize={0.15}
        position={[0, 2.6, 0]}
        color="#94a3b8"
        anchorX="center"
        anchorY="middle"
    />
</T.Group>
