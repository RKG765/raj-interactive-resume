/**
 * Global state for the portfolio using Svelte 5 runes.
 * Module-level $state is reactive across all importing components.
 * Currently terminal-only; 3D scene mode will be added later.
 */

export type Mode = 'terminal';
export type Theme = 'dark';

let mode = $state<Mode>('terminal');
let theme = $state<Theme>('dark');

export function getMode(): Mode {
    return mode;
}

export function getTheme(): Theme {
    return theme;
}
