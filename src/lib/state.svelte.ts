/**
 * Global state for the portfolio using Svelte 5 runes.
 * Module-level $state is reactive across all importing components.
 */

export type Mode = 'terminal' | 'scene';
export type Theme = 'dark' | 'light';

let mode = $state<Mode>('terminal');
let theme = $state<Theme>('dark');
let transitioning = $state(false);

export function getMode(): Mode {
    return mode;
}

export function getTheme(): Theme {
    return theme;
}

export function isTransitioning(): boolean {
    return transitioning;
}

export function toggleMode() {
    transitioning = true;
    setTimeout(() => {
        mode = mode === 'terminal' ? 'scene' : 'terminal';
        theme = mode === 'terminal' ? 'dark' : 'light';
        setTimeout(() => {
            transitioning = false;
        }, 100);
    }, 400);
}

export function setMode(newMode: Mode) {
    mode = newMode;
    theme = newMode === 'terminal' ? 'dark' : 'light';
}
