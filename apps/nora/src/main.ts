import './styles.css';
import { evolveLexicon, type RuleWeights } from './rules';

const DEFAULT_LEXICON = `luma
astra
vara
keth
sora`; // newline separated

const DEFAULT_WEIGHTS: RuleWeights = {
  ritual: 0.6,
  trade: 0.5,
  symbolism: 0.7,
  hierarchy: 0.4
};

function toCsv(rows: ReturnType<typeof evolveLexicon>): string {
  const header = 'original,transformed,rulesApplied,culturalImprint';
  const body = rows
    .map((row) => {
      const rules = row.rulesApplied.join('|');
      return [row.original, row.transformed, rules, row.culturalImprint.toFixed(2)]
        .map((value) => `"${value.replace(/"/g, '""')}"`)
        .join(',');
    })
    .join('\n');
  return `${header}\n${body}`;
}

function render(): void {
  const app = document.getElementById('app');
  if (!app) return;

  app.innerHTML = '';

  const intro = document.createElement('section');
  intro.className = 'panel';
  const title = document.createElement('h1');
  title.textContent = 'NΦRA Symbolic Interpreter';
  const description = document.createElement('p');
  description.textContent = 'Define a lexicon, tune cultural weights, and explore how symbolic rules evolve each entry.';
  intro.appendChild(title);
  intro.appendChild(description);

  const textarea = document.createElement('textarea');
  textarea.value = DEFAULT_LEXICON;
  textarea.setAttribute('aria-label', 'Seed lexicon words, one per line');
  intro.appendChild(textarea);

  const controls = document.createElement('section');
  controls.className = 'panel';

  const weights: RuleWeights = { ...DEFAULT_WEIGHTS };

  const sliderContainer = document.createElement('div');
  sliderContainer.className = 'controls';

  (['ritual', 'trade', 'symbolism', 'hierarchy'] as const).forEach((key) => {
    const control = document.createElement('div');
    control.className = 'control';
    const label = document.createElement('label');
    label.textContent = key.charAt(0).toUpperCase() + key.slice(1);
    label.setAttribute('for', `slider-${key}`);

    const valueBadge = document.createElement('strong');
    valueBadge.textContent = weights[key].toFixed(2);

    const slider = document.createElement('input');
    slider.type = 'range';
    slider.id = `slider-${key}`;
    slider.min = '0';
    slider.max = '1';
    slider.step = '0.01';
    slider.value = weights[key].toString();
    slider.addEventListener('input', () => {
      weights[key] = Number.parseFloat(slider.value);
      valueBadge.textContent = weights[key].toFixed(2);
      update();
    });

    const headerRow = document.createElement('div');
    headerRow.style.display = 'flex';
    headerRow.style.justifyContent = 'space-between';
    headerRow.appendChild(label);
    headerRow.appendChild(valueBadge);

    control.appendChild(headerRow);
    control.appendChild(slider);
    sliderContainer.appendChild(control);
  });

  controls.appendChild(sliderContainer);

  const actions = document.createElement('div');
  actions.className = 'actions';

  const regenerateButton = document.createElement('button');
  regenerateButton.type = 'button';
  regenerateButton.textContent = 'Regenerate';
  regenerateButton.addEventListener('click', () => update());

  const downloadButton = document.createElement('button');
  downloadButton.type = 'button';
  downloadButton.className = 'secondary';
  downloadButton.textContent = 'Download CSV';
  downloadButton.addEventListener('click', () => {
    const csv = toCsv(results);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'nora-evolved.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });

  actions.appendChild(regenerateButton);
  actions.appendChild(downloadButton);
  controls.appendChild(actions);

  const tablePanel = document.createElement('section');
  tablePanel.className = 'panel';
  const tableHeading = document.createElement('h2');
  tableHeading.textContent = 'Lexicon Evolution';
  tablePanel.appendChild(tableHeading);

  const table = document.createElement('table');
  const thead = document.createElement('thead');
  thead.innerHTML = '<tr><th>Original</th><th>Transformed</th><th>Rules</th><th>Cultural Imprint</th></tr>';
  const tbody = document.createElement('tbody');
  table.appendChild(thead);
  table.appendChild(tbody);
  tablePanel.appendChild(table);

  app.appendChild(intro);
  app.appendChild(controls);
  app.appendChild(tablePanel);

  let results = evolveLexicon(textarea.value.split('\n'), weights, 9);

  function update(): void {
    results = evolveLexicon(textarea.value.split('\n'), weights, 9);
    tbody.innerHTML = '';
    results.forEach((row) => {
      const tr = document.createElement('tr');
      const rules = row.rulesApplied.length ? row.rulesApplied.join(', ') : '—';
      tr.innerHTML = `<td>${row.original}</td><td>${row.transformed}</td><td>${rules}</td><td>${row.culturalImprint.toFixed(
        2
      )}</td>`;
      tbody.appendChild(tr);
    });
  }

  textarea.addEventListener('input', () => update());
  update();
}

render();
