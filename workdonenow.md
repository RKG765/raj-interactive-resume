# Work Done — Portfolio Terminal (Feb 22, 2026)

## 1. Terminal Layout Fix
- Replaced ASCII box borders (`╔══╗`, `║`) with CSS-styled containers
- Full-width responsive layout — no fixed pixel widths
- `pre { white-space: pre-wrap; word-wrap: break-word }` prevents overflow
- Responsive font scaling for mobile/desktop
- Custom scrollbar, scanline overlay, cursor blink animation

## 2. Removed 3D Scene & Light Mode
- Stripped all Scene/Threlte code from `+layout.svelte`
- Removed `toggleMode`, `isTransitioning` from `state.svelte.ts`
- State is now terminal-only (`mode: 'terminal'`, `theme: 'dark'`)
- Scene component files kept in repo for future use

## 3. Removed GitHubTracker Auto-Ticker
- Removed `GitHubTracker.svelte` from layout
- Was auto-fetching from GitHub API on page load (rate-limit risk)
- Replaced with on-demand `projects` command (see below)

## 4. Professional Command Overhaul
Old commands removed: `cat pygit.md`, `run job_scraper`, `view lld_notes`, `ssh ai_gateway`

New command set (all client-side, no backend needed):

| Command        | Description                    |
|----------------|--------------------------------|
| `help`         | Show all commands              |
| `clear`        | Clear terminal                 |
| `whoami`       | About Raj Kumar                |
| `resume`       | Summary resume                 |
| `skills`       | Tech stack grouped by domain   |
| `experience`   | Work & major projects          |
| `education`    | Academic background            |
| `architecture` | System design philosophy       |
| `devops`       | CI/CD, Docker, infra knowledge |
| `systems`      | Low-level & performance work   |
| `projects`     | **Live GitHub repos (dynamic)**|
| `contact`      | Email, GitHub, LinkedIn        |
| `github`       | Opens GitHub in new tab        |
| `linkedin`     | Opens LinkedIn in new tab      |
| `history`      | Show command history           |

## 5. Backend `/api/projects` Endpoint
- Replaced old `/api/github` (events) with `/api/projects` (repos)
- Fetches from `github.com/RKG765`, filters forks & archived repos
- Normalizes to clean objects: `name`, `description`, `tech`, `stars`, `url`
- **10-minute in-memory cache** — serves stale data on API failure
- Removed old `/api/commands` endpoint (commands are now client-side)

## 6. Terminal Text Selection Fix
- Changed `onclick` to `onmouseup` with `window.getSelection()` check
- Added `user-select: text` to output area
- Users can now select and copy terminal text

## 7. README Updated
- Added Mermaid diagrams for architecture, runtime flow
- Added tech stack rationale comparison tables
- Added Vercel deployment instructions

## Files Modified
- `src/lib/components/Terminal.svelte` — Full rewrite
- `src/routes/+layout.svelte` — Simplified to terminal-only
- `src/lib/state.svelte.ts` — Stripped to terminal/dark only
- `api/index.py` — New `/api/projects`, removed `/api/commands` & `/api/github`
- `README.md` — Architecture docs added
