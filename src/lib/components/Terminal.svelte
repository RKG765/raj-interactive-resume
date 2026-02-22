<script lang="ts">
    import { onMount, tick } from "svelte";

    // ── State ─────────────────────────────────────────
    interface TermLine {
        type: "input" | "output" | "error" | "system" | "chat-in" | "chat-out";
        content: string;
        style?: string;
    }

    let lines = $state<TermLine[]>([
        {
            type: "system",
            content: `
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       ██████╗  ██████╗ ██████╗ ████████╗                     ║
║       ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝                     ║
║       ██████╔╝██║   ██║██████╔╝   ██║                        ║
║       ██╔═══╝ ██║   ██║██╔══██╗   ██║                        ║
║       ██║     ╚██████╔╝██║  ██║   ██║                        ║
║       ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝                        ║
║                                                              ║
║   Raj Kumar's Portfolio Terminal v2.0                         ║
║   Type 'help' for available commands                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝`,
        },
    ]);

    let currentInput = $state("");
    let commandHistory = $state<string[]>([]);
    let historyIndex = $state(-1);
    let isLoading = $state(false);
    let chatMode = $state(false);
    let chatHistory = $state<{ role: string; content: string }[]>([]);

    let terminalEl: HTMLDivElement;
    let inputEl: HTMLInputElement;

    // ── Auto-scroll ────────────────────────────────────
    $effect(() => {
        // Track lines length to trigger scroll
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

        if (chatMode) {
            await handleChat(cmd);
            return;
        }

        lines.push({ type: "input", content: `❯ ${cmd}` });
        commandHistory = [...commandHistory, cmd];
        historyIndex = -1;
        currentInput = "";

        if (cmd.toLowerCase() === "clear") {
            lines = [];
            return;
        }

        isLoading = true;

        try {
            const res = await fetch("/api/commands", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd }),
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();

            if (data.type === "chat_init") {
                lines.push({
                    type: "output",
                    content: data.content,
                    style: data.style,
                });
                chatMode = true;
                chatHistory = [];
            } else if (data.type === "error") {
                lines.push({ type: "error", content: data.content });
            } else {
                lines.push({
                    type: "output",
                    content: data.content,
                    style: data.style,
                });
            }
        } catch (err) {
            lines.push({
                type: "error",
                content: `⚠️  Network error. Backend may be offline.\n   ${err}`,
            });
        } finally {
            isLoading = false;
        }
    }

    async function handleChat(message: string) {
        if (message.toLowerCase() === "exit") {
            lines.push({ type: "chat-in", content: `you> ${message}` });
            lines.push({
                type: "system",
                content: "🔐 SSH session terminated. Connection closed.",
            });
            chatMode = false;
            chatHistory = [];
            currentInput = "";
            return;
        }

        lines.push({ type: "chat-in", content: `you> ${message}` });
        chatHistory = [...chatHistory, { role: "user", content: message }];
        currentInput = "";
        isLoading = true;

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, history: chatHistory }),
            });

            const data = await res.json();
            const reply = data.reply || "No response";
            lines.push({ type: "chat-out", content: `ai> ${reply}` });
            chatHistory = [
                ...chatHistory,
                { role: "assistant", content: reply },
            ];
        } catch {
            lines.push({
                type: "error",
                content: "⚠️  Failed to reach AI Gateway",
            });
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
        inputEl?.focus();
    }

    // ── Helpers ─────────────────────────────────────────
    function getLineColor(line: TermLine): string {
        switch (line.type) {
            case "input":
                return "text-cyber-amber";
            case "error":
                return "text-red-400";
            case "system":
                return "text-cyber-green glow-text";
            case "chat-in":
                return "text-cyan-400";
            case "chat-out":
                return "text-cyber-green";
            default:
                return "text-cyber-text";
        }
    }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
    class="terminal-glow flex h-full flex-col bg-cyber-bg"
    onclick={focusInput}
>
    <!-- Terminal Header Bar -->
    <div
        class="flex items-center gap-2 border-b border-cyber-border/50 bg-cyber-surface/80 px-4 py-2.5"
    >
        <div class="flex gap-1.5">
            <div class="h-3 w-3 rounded-full bg-red-500/80"></div>
            <div class="h-3 w-3 rounded-full bg-yellow-500/80"></div>
            <div class="h-3 w-3 rounded-full bg-green-500/80"></div>
        </div>
        <div class="flex-1 text-center">
            <span class="text-xs font-medium text-cyber-text/50">
                {chatMode
                    ? "🔐 ai_gateway — ssh session"
                    : "⌘ raj@portfolio ~ bash"}
            </span>
        </div>
        <div class="text-[10px] text-cyber-green/40">
            {chatMode ? "CHAT" : "TERM"}
        </div>
    </div>

    <!-- Terminal Output -->
    <div
        bind:this={terminalEl}
        class="flex-1 overflow-y-auto p-4 font-mono text-sm leading-relaxed"
    >
        {#each lines as line, i}
            <div class="animate-[fade-up_0.15s_ease-out] {getLineColor(line)}">
                <pre
                    class="whitespace-pre-wrap break-words font-mono">{line.content}</pre>
            </div>
        {/each}

        {#if isLoading}
            <div class="flex items-center gap-2 py-2 text-cyber-green/60">
                <div class="flex gap-1">
                    <span
                        class="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-cyber-green/60"
                        style="animation-delay: 0ms;"
                    ></span>
                    <span
                        class="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-cyber-green/60"
                        style="animation-delay: 150ms;"
                    ></span>
                    <span
                        class="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-cyber-green/60"
                        style="animation-delay: 300ms;"
                    ></span>
                </div>
                <span class="text-xs">Processing...</span>
            </div>
        {/if}
    </div>

    <!-- Input Line -->
    <div
        class="flex items-center border-t border-cyber-border/30 bg-cyber-surface/40 px-4 py-3"
    >
        <span
            class="mr-2 text-sm font-bold {chatMode
                ? 'text-cyan-400'
                : 'text-cyber-green'}"
        >
            {chatMode ? "you❯" : "❯"}
        </span>
        <input
            bind:this={inputEl}
            bind:value={currentInput}
            onkeydown={handleKeyDown}
            disabled={isLoading}
            type="text"
            class="flex-1 border-none bg-transparent font-mono text-sm text-cyber-green outline-none placeholder:text-cyber-text/20 caret-cyber-green"
            placeholder={chatMode
                ? "Type a message... (exit to disconnect)"
                : "Type a command..."}
            spellcheck="false"
            autocomplete="off"
        />
        <span class="cursor-blink ml-1 text-cyber-green">▊</span>
    </div>

    <!-- Scanline Overlay -->
    <div
        class="pointer-events-none absolute inset-0 overflow-hidden opacity-[0.03]"
    >
        <div
            class="h-[2px] w-full bg-cyber-green"
            style="animation: scanline 8s linear infinite;"
        ></div>
    </div>
</div>
