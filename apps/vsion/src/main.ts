import './styles.css';
import { simulate, type SimulationParams } from './sim';
import { createApp } from './ui';

const DEFAULT_PARAMS: SimulationParams = {
  ritual: 0.6,
  trade: 0.4,
  symbolism: 0.7,
  hierarchy: 0.5
};

function parseHash(): SimulationParams {
  const hash = window.location.hash.replace(/^#/, '');
  const params = new URLSearchParams(hash);
  const result: SimulationParams = { ...DEFAULT_PARAMS };
  (['ritual', 'trade', 'symbolism', 'hierarchy'] as const).forEach((key) => {
    const value = params.get(key);
    if (value !== null) {
      const numeric = Number.parseFloat(value);
      if (!Number.isNaN(numeric)) {
        result[key] = Math.min(1, Math.max(0, numeric));
      }
    }
  });
  return result;
}

function serializeParams(params: SimulationParams): string {
  const search = new URLSearchParams();
  (['ritual', 'trade', 'symbolism', 'hierarchy'] as const).forEach((key) => {
    search.set(key, params[key].toFixed(2));
  });
  return search.toString();
}

function main(): void {
  const container = document.body;
  const root = document.createElement('div');
  container.innerHTML = '';
  container.appendChild(root);

  let currentParams = parseHash();
  const app = createApp(root, currentParams, (next) => {
    currentParams = next;
    const result = simulate(currentParams, { seed: 42 });
    app.update(result);
  });

  const initialResult = simulate(currentParams, { seed: 42 });
  app.update(initialResult);

  app.setShareHandler(async () => {
    const hash = serializeParams(currentParams);
    window.location.hash = hash;
    const shareUrl = `${window.location.origin}${window.location.pathname}#${hash}`;
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(shareUrl);
      }
      alert('Shareable link copied to clipboard!');
    } catch (error) {
      console.warn('Unable to copy link', error);
    }
  });

  window.addEventListener('hashchange', () => {
    currentParams = parseHash();
    const result = simulate(currentParams, { seed: 42 });
    app.update(result);
  });
}

main();
