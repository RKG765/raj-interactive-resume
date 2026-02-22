<script lang="ts">
    import { onMount, tick } from "svelte";

    // ── State ─────────────────────────────────────────
    interface TermLine {
        type: "input" | "output" | "error" | "system";
        content: string;
    }

    let lines = $state<TermLine[]>([
        {
            type: "system",
            content: `
  ██████╗  ██████╗ ██████╗ ████████╗
  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
  ██████╔╝██║   ██║██████╔╝   ██║
  ██╔═══╝ ██║   ██║██╔══██╗   ██║
  ██║     ╚██████╔╝██║  ██║   ██║
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝

  Raj Kumar — Portfolio Terminal v2.0
  Type 'help' for available commands`,
        },
    ]);

    let currentInput = $state("");
    let commandHistory = $state<string[]>([]);
    let historyIndex = $state(-1);
    let isLoading = $state(false);

    let terminalEl: HTMLDivElement;
    let inputEl: HTMLInputElement;

    // ── Command Data ────────────────────────────────────

    const HELP_TEXT = `Available commands:

  Identity
    whoami         About me
    resume         Summary resume
    skills         Tech stack by domain
    experience     Work & major projects
    education      Academic background

  Work
    projects       Featured GitHub repos (live)
    architecture   System design philosophy
    devops         CI/CD, Docker, infra
    systems        Low-level & performance work

  Contact
    contact        Email, GitHub, LinkedIn
    github         Open GitHub profile
    linkedin       Open LinkedIn profile

  Utility
    help           Show this message
    clear          Clear terminal
    history        Command history`;

    const WHOAMI = `  Raj Kumar
  Full-Stack Developer & Systems Thinker

  B.Tech CSE @ BML Munjal University
  Focus: Backend Systems, DevOps, AI/ML

  "Learning for the purpose of learning."

  I build tools to understand how they work —
  from version control internals to AI security
  gateways. Every project is a deep-dive into
  the fundamentals, not just the framework.

  github.com/RKG765`;

    const RESUME = `  ━━━ RAJ KUMAR ━━━━━━━━━━━━━━━━━━━━

  Full-Stack Developer & Systems Thinker
  B.Tech CSE — BML Munjal University

  Core Strengths:
  • Backend architecture (FastAPI, Node.js)
  • DevOps & infrastructure (Docker, AWS, CI/CD)
  • AI/ML pipelines & data engineering
  • Systems programming (Python, C++)

  Notable Work:
  • PyGit — Git internals from scratch (Python)
  • Job Scraper — Distributed crawler + REST API
  • AI Gateway — Secure LLM proxy with rate limiting
  • Food Fraud Detector — CNN + feature fusion pipeline

  Contact: github.com/RKG765`;

    const SKILLS = `  ━━━ LANGUAGES ━━━━━━━━━━━━━━━━━━━━
  Python · C++ · JavaScript · TypeScript · SQL

  ━━━ BACKEND ━━━━━━━━━━━━━━━━━━━━━━
  FastAPI · Node.js · Express · REST · WebSockets
  PostgreSQL · Redis · Celery · SQLAlchemy

  ━━━ FRONTEND ━━━━━━━━━━━━━━━━━━━━━
  SvelteKit · React · Tailwind · Three.js

  ━━━ DEVOPS & INFRA ━━━━━━━━━━━━━━━
  Docker · AWS (EC2, S3, Lambda) · GitHub Actions
  Nginx · Linux · CI/CD Pipelines

  ━━━ AI / ML ━━━━━━━━━━━━━━━━━━━━━━
  PyTorch · Hugging Face · Stable Diffusion
  CNNs · Feature Extraction · Data Pipelines

  ━━━ TOOLS ━━━━━━━━━━━━━━━━━━━━━━━━
  Git · Postman · Scrapy · Vercel · Ghidra`;

    const EXPERIENCE = `  ━━━ PROJECTS & EXPERIENCE ━━━━━━━━

  PyGit — Python Version Control System
  • Built Git internals from scratch: blob store,
    commit DAG, three-way merge, Myers diff
  • 2,400+ lines of pure Python
  • github.com/RKG765/pygit

  Job Scraper — Distributed Job Aggregator
  • Scrapy spiders → FastAPI REST → PostgreSQL
  • Redis caching, Celery scheduling, Razorpay billing
  • Deduplication pipeline with fuzzy matching

  AI Security Gateway — Secure LLM Proxy
  • FastAPI middleware for Groq LLaMA integration
  • Prompt injection defense, API key rotation
  • Rate limiting, streaming response proxying

  Food Fraud Detector — AI Image Analysis
  • CNN binary classifier + FFT/CLIP feature fusion
  • Stable Diffusion inpainting for training data
  • End-to-end ML pipeline with PyTorch

  Type 'projects' for live GitHub data.`;

    const EDUCATION = `  ━━━ EDUCATION ━━━━━━━━━━━━━━━━━━━━

  B.Tech Computer Science & Engineering
  BML Munjal University, Gurugram

  Relevant Coursework:
  • Data Structures & Algorithms
  • Operating Systems
  • Computer Networks
  • Database Management Systems
  • Object-Oriented Programming (C++)
  • Machine Learning
  • Software Engineering

  Self-Directed Learning:
  • System Design & LLD patterns
  • Docker & container orchestration
  • AI/ML pipeline architecture
  • Security & reverse engineering`;

    const ARCHITECTURE = `  ━━━ SYSTEM DESIGN PHILOSOPHY ━━━━━

  Principles I follow:
  • Build from scratch before using frameworks
  • Understand the abstraction layer below
  • Design for failure, not just success
  • Cache aggressively, validate early

  Architecture Patterns:
  • Event-driven (Observer, Pub/Sub)
  • Layered (Controller → Service → Repository)
  • Pipeline (ETL, ML feature extraction)
  • Proxy (API Gateway, reverse proxy)

  Example — This Portfolio:
  • SvelteKit static frontend (Vercel CDN)
  • FastAPI serverless backend (Vercel Functions)
  • GitHub API proxy with in-memory caching
  • Terminal UI as primary interaction model

  I design systems to be understood, not just used.`;

    const DEVOPS = `  ━━━ DEVOPS & INFRASTRUCTURE ━━━━━━

  Containerization:
  • Docker multi-stage builds
  • Docker Compose for local dev stacks
  • Container security best practices

  CI/CD:
  • GitHub Actions workflows
  • Automated testing + linting
  • Zero-downtime deployment strategies

  Cloud:
  • AWS EC2, S3, Lambda, CloudFront
  • Vercel serverless functions
  • Nginx reverse proxy configuration

  Monitoring & Observability:
  • Structured logging
  • Health check endpoints
  • Error tracking & alerting

  Security:
  • API key rotation patterns
  • Rate limiting middleware
  • Input sanitization & validation`;

    const SYSTEMS = `  ━━━ SYSTEMS & LOW-LEVEL WORK ━━━━━

  PyGit — Version Control Internals
  • SHA-1 content-addressable blob store
  • Binary index file format parsing
  • DAG traversal for commit history
  • Myers diff algorithm implementation
  • Three-way merge with conflict detection

  LLD & Design Patterns (C++):
  • SOLID principles applied in practice
  • Singleton, Factory, Observer, Strategy
  • State machines for complex workflows
  • Smart pointers & RAII patterns

  Reverse Engineering:
  • Ghidra for native library analysis
  • APK decompilation & analysis
  • Understanding anti-analysis techniques

  Performance:
  • Algorithmic complexity optimization
  • Memory-efficient data structures
  • Profiling & bottleneck identification`;

    const CONTACT = `  ━━━ CONTACT ━━━━━━━━━━━━━━━━━━━━━━

  GitHub    github.com/RKG765
  LinkedIn  linkedin.com/in/rajkumar
  Email     rajkumar@example.com

  Open to backend, DevOps, and AI/ML roles.
  Prefer systems-level work over pure frontend.`;

    const LOCAL_COMMANDS: Record<string, string> = {
        whoami: WHOAMI,
        resume: RESUME,
        skills: SKILLS,
        experience: EXPERIENCE,
        education: EDUCATION,
        architecture: ARCHITECTURE,
        devops: DEVOPS,
        systems: SYSTEMS,
        contact: CONTACT,
    };

    // ── Auto-scroll ────────────────────────────────────
    $effect(() => {
        const _ = lines.length;
        tick().then(() => {
            if (terminalEl) {
                terminalEl.scrollTop = terminalEl.scrollHeight;
            }
        });
    });

    onMount(() => {
        inputEl?.focus();
    });

    // ── Command Processing ─────────────────────────────
    async function processCommand() {
        const cmd = currentInput.trim();
        if (!cmd) return;

        lines.push({ type: "input", content: `❯ ${cmd}` });
        commandHistory = [...commandHistory, cmd];
        historyIndex = -1;
        currentInput = "";

        const cmdLower = cmd.toLowerCase();

        // ── Utility commands ──
        if (cmdLower === "clear") {
            lines = [];
            return;
        }

        if (cmdLower === "help") {
            lines.push({ type: "output", content: HELP_TEXT });
            return;
        }

        if (cmdLower === "history") {
            const hist =
                commandHistory.length > 1
                    ? commandHistory
                          .slice(0, -1)
                          .map((c, i) => `  ${i + 1}  ${c}`)
                          .join("\n")
                    : "  No previous commands.";
            lines.push({ type: "output", content: hist });
            return;
        }

        // ── External link commands ──
        if (cmdLower === "github") {
            window.open("https://github.com/RKG765", "_blank");
            lines.push({
                type: "system",
                content: "  Opening github.com/RKG765...",
            });
            return;
        }

        if (cmdLower === "linkedin") {
            window.open("https://linkedin.com/in/rajkumar", "_blank");
            lines.push({
                type: "system",
                content: "  Opening LinkedIn profile...",
            });
            return;
        }

        // ── Dynamic projects command ──
        if (cmdLower === "projects") {
            await fetchProjects();
            return;
        }

        // ── Static local commands ──
        if (cmdLower in LOCAL_COMMANDS) {
            lines.push({ type: "output", content: LOCAL_COMMANDS[cmdLower] });
            return;
        }

        // ── Unknown command ──
        lines.push({
            type: "error",
            content: `  Command not found: ${cmd}\n  Type 'help' for available commands.`,
        });
    }

    async function fetchProjects() {
        isLoading = true;
        try {
            const res = await fetch("/api/projects");
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();
            const repos = data.projects || [];

            if (repos.length === 0) {
                lines.push({
                    type: "output",
                    content: "  No featured projects found.",
                });
                return;
            }

            let output = "  ━━━ FEATURED PROJECTS ━━━━━━━━━━━\n";
            for (const repo of repos) {
                output += `\n  ${repo.name}`;
                if (repo.stars > 0) output += ` ★${repo.stars}`;
                output += `\n  ${repo.description || "No description"}`;
                if (repo.tech && repo.tech.length > 0) {
                    output += `\n  [${repo.tech.join(" · ")}]`;
                }
                output += `\n  ${repo.url}`;
                output += `\n`;
            }

            lines.push({ type: "output", content: output });
        } catch {
            // Fallback: try direct GitHub API (client-side)
            try {
                const res = await fetch(
                    "https://api.github.com/users/RKG765/repos?sort=updated&per_page=10",
                    { headers: { Accept: "application/vnd.github.v3+json" } },
                );
                if (!res.ok) throw new Error();
                const repos = await res.json();
                const filtered = repos.filter(
                    (r: any) => !r.fork && !r.archived,
                );

                let output = "  ━━━ FEATURED PROJECTS ━━━━━━━━━━━\n";
                for (const repo of filtered.slice(0, 8)) {
                    output += `\n  ${repo.name}`;
                    if (repo.stargazers_count > 0)
                        output += ` ★${repo.stargazers_count}`;
                    output += `\n  ${repo.description || "No description"}`;
                    if (repo.language) output += `\n  [${repo.language}]`;
                    output += `\n  ${repo.html_url}`;
                    output += `\n`;
                }

                lines.push({ type: "output", content: output });
            } catch {
                lines.push({
                    type: "error",
                    content: "  ⚠ Could not fetch projects. Try again later.",
                });
            }
        } finally {
            isLoading = false;
        }
    }

    function handleKeyDown(e: KeyboardEvent) {
        if (e.key === "Enter") {
            e.preventDefault();
            processCommand();
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            if (commandHistory.length === 0) return;
            if (historyIndex === -1) historyIndex = commandHistory.length - 1;
            else if (historyIndex > 0) historyIndex--;
            currentInput = commandHistory[historyIndex];
        } else if (e.key === "ArrowDown") {
            e.preventDefault();
            if (historyIndex === -1) return;
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                currentInput = commandHistory[historyIndex];
            } else {
                historyIndex = -1;
                currentInput = "";
            }
        } else if (e.key === "l" && e.ctrlKey) {
            e.preventDefault();
            lines = [];
        }
    }

    function focusInput() {
        const selection = window.getSelection();
        if (!selection || selection.toString().length === 0) {
            inputEl?.focus();
        }
    }

    function getLineColor(line: TermLine): string {
        switch (line.type) {
            case "input":
                return "text-cyber-amber";
            case "error":
                return "text-red-400";
            case "system":
                return "text-cyber-green glow-text";
            default:
                return "text-cyber-text";
        }
    }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="terminal-container" onmouseup={focusInput}>
    <!-- Header Bar -->
    <div class="terminal-header">
        <div class="header-dots">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
        </div>
        <div class="header-title">raj@portfolio ~ bash</div>
        <div class="header-badge">TERM</div>
    </div>

    <!-- Output -->
    <div bind:this={terminalEl} class="terminal-output">
        {#each lines as line}
            <div class="line {getLineColor(line)}">
                <pre>{line.content}</pre>
            </div>
        {/each}

        {#if isLoading}
            <div class="loading-indicator">
                <div class="loading-dots">
                    <span class="bounce-dot" style="animation-delay: 0ms;"
                    ></span>
                    <span class="bounce-dot" style="animation-delay: 150ms;"
                    ></span>
                    <span class="bounce-dot" style="animation-delay: 300ms;"
                    ></span>
                </div>
                <span class="loading-text">Fetching...</span>
            </div>
        {/if}
    </div>

    <!-- Input -->
    <div class="terminal-input">
        <span class="prompt">❯</span>
        <input
            bind:this={inputEl}
            bind:value={currentInput}
            onkeydown={handleKeyDown}
            disabled={isLoading}
            type="text"
            class="input-field"
            placeholder="Type a command..."
            spellcheck="false"
            autocomplete="off"
        />
        <span class="cursor-blink">▊</span>
    </div>

    <!-- Scanline Overlay -->
    <div class="scanline-overlay">
        <div class="scanline-bar"></div>
    </div>
</div>

<style>
    .terminal-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        background: var(--cyber-bg, #0a0e17);
        position: relative;
        overflow: hidden;
    }

    .terminal-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid rgba(0, 255, 65, 0.15);
        background: rgba(13, 17, 28, 0.8);
        padding: 0.625rem 1rem;
        flex-shrink: 0;
    }

    .header-dots {
        display: flex;
        gap: 6px;
    }

    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .dot-red {
        background: rgba(239, 68, 68, 0.8);
    }
    .dot-yellow {
        background: rgba(234, 179, 8, 0.8);
    }
    .dot-green {
        background: rgba(34, 197, 94, 0.8);
    }

    .header-title {
        flex: 1;
        text-align: center;
        font-size: 0.75rem;
        font-weight: 500;
        color: rgba(180, 190, 210, 0.5);
    }

    .header-badge {
        font-size: 10px;
        color: rgba(0, 255, 65, 0.4);
    }

    .terminal-output {
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 1rem;
        font-family: "Courier New", "Fira Code", monospace;
        font-size: 0.8rem;
        line-height: 1.6;
        user-select: text;
        -webkit-user-select: text;
    }

    .terminal-output pre {
        margin: 0;
        font-family: inherit;
        font-size: inherit;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }

    .line {
        animation: fade-up 0.12s ease-out;
    }

    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0;
        color: rgba(0, 255, 65, 0.6);
    }

    .loading-dots {
        display: flex;
        gap: 4px;
    }

    .bounce-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(0, 255, 65, 0.6);
        animation: bounce 1s infinite;
    }

    .loading-text {
        font-size: 0.75rem;
    }

    .terminal-input {
        display: flex;
        align-items: center;
        border-top: 1px solid rgba(0, 255, 65, 0.15);
        background: rgba(13, 17, 28, 0.4);
        padding: 0.75rem 1rem;
        flex-shrink: 0;
    }

    .prompt {
        margin-right: 0.5rem;
        font-size: 0.875rem;
        font-weight: bold;
        color: var(--cyber-green, #00ff41);
    }

    .input-field {
        flex: 1;
        border: none;
        background: transparent;
        font-family: "Courier New", "Fira Code", monospace;
        font-size: 0.875rem;
        color: var(--cyber-green, #00ff41);
        outline: none;
        caret-color: var(--cyber-green, #00ff41);
    }

    .input-field::placeholder {
        color: rgba(180, 190, 210, 0.2);
    }

    .cursor-blink {
        margin-left: 4px;
        color: var(--cyber-green, #00ff41);
        animation: cursor-blink 1s step-end infinite;
    }

    .scanline-overlay {
        pointer-events: none;
        position: absolute;
        inset: 0;
        overflow: hidden;
        opacity: 0.03;
    }

    .scanline-bar {
        height: 2px;
        width: 100%;
        background: var(--cyber-green, #00ff41);
        animation: scanline 8s linear infinite;
    }

    .terminal-output::-webkit-scrollbar {
        width: 6px;
    }
    .terminal-output::-webkit-scrollbar-track {
        background: transparent;
    }
    .terminal-output::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 65, 0.2);
        border-radius: 3px;
    }
    .terminal-output::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 65, 0.4);
    }

    @media (max-width: 640px) {
        .terminal-output {
            font-size: 0.65rem;
            padding: 0.5rem;
        }
        .terminal-output pre {
            font-size: 0.65rem;
        }
        .terminal-input {
            padding: 0.5rem 0.75rem;
        }
    }

    @media (min-width: 1200px) {
        .terminal-output {
            font-size: 0.875rem;
        }
        .terminal-output pre {
            font-size: 0.875rem;
        }
    }

    :global(.text-cyber-amber) {
        color: var(--cyber-amber, #f59e0b);
    }
    :global(.text-red-400) {
        color: #f87171;
    }
    :global(.text-cyber-green) {
        color: var(--cyber-green, #00ff41);
    }
    :global(.text-cyber-text) {
        color: var(--cyber-text, #b4bed2);
    }
    :global(.glow-text) {
        text-shadow: 0 0 10px var(--cyber-green, #00ff41);
    }

    @keyframes fade-up {
        from {
            opacity: 0;
            transform: translateY(4px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes bounce {
        0%,
        80%,
        100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-6px);
        }
    }

    @keyframes cursor-blink {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0;
        }
    }

    @keyframes scanline {
        0% {
            transform: translateY(-100%);
        }
        100% {
            transform: translateY(100vh);
        }
    }
</style>
