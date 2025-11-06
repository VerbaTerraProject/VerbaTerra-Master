import './styles.css';
import { parseCsvFile, parseCsvText } from './csv';
import { enrichRecords, type CulturalRecord } from './metrics';
import { createCharts } from './charts';

async function loadSample(): Promise<CulturalRecord[]> {
  const response = await fetch('./example.csv');
  const text = await response.text();
  return parseCsvText(text);
}

function createTable(records: ReturnType<typeof enrichRecords>): HTMLTableSectionElement {
  const tbody = document.createElement('tbody');
  records.forEach((record) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${record.label}</td>
      <td>${record.ritual.toFixed(2)}</td>
      <td>${record.trade.toFixed(2)}</td>
      <td>${record.symbolism.toFixed(2)}</td>
      <td>${record.hierarchy.toFixed(2)}</td>
      <td>${record.diversity.toFixed(2)}</td>
      <td>${record.multilinguality.toFixed(2)}</td>
      <td>${record.hybridity.toFixed(2)}</td>
      <td>${record.nlis.toFixed(2)}</td>
      <td>${record.crm.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });
  return tbody;
}

async function bootstrap(): Promise<void> {
  const app = document.getElementById('app');
  if (!app) return;
  app.innerHTML = '';

  const header = document.createElement('header');
  const h1 = document.createElement('h1');
  h1.textContent = 'VerbaTerra Analyst';
  const subtitle = document.createElement('p');
  subtitle.textContent = 'Upload CSV data, infer schema automatically, and inspect NLIS and CRM cultural indicators.';
  header.appendChild(h1);
  header.appendChild(subtitle);

  const controls = document.createElement('section');
  controls.className = 'controls';

  const uploadRow = document.createElement('div');
  uploadRow.className = 'upload';
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '.csv';
  fileInput.setAttribute('aria-label', 'Upload CSV file');

  const sampleButton = document.createElement('button');
  sampleButton.type = 'button';
  sampleButton.textContent = 'Try sample data';

  const status = document.createElement('span');
  status.textContent = 'Awaiting data…';
  status.style.fontWeight = '600';

  uploadRow.appendChild(fileInput);
  uploadRow.appendChild(sampleButton);
  uploadRow.appendChild(status);
  controls.appendChild(uploadRow);

  const chartsSection = document.createElement('section');
  chartsSection.className = 'section';
  const chartsHeading = document.createElement('h2');
  chartsHeading.textContent = 'Metrics';
  chartsSection.appendChild(chartsHeading);

  const chartGrid = document.createElement('div');
  chartGrid.className = 'charts';
  const distributionCanvas = document.createElement('canvas');
  distributionCanvas.setAttribute('aria-label', 'NLIS distribution chart');
  const scatterCanvas = document.createElement('canvas');
  scatterCanvas.setAttribute('aria-label', 'NLIS versus CRM scatter plot');
  chartGrid.appendChild(distributionCanvas);
  chartGrid.appendChild(scatterCanvas);
  chartsSection.appendChild(chartGrid);

  const tableSection = document.createElement('section');
  tableSection.className = 'section';
  const tableHeading = document.createElement('h2');
  tableHeading.textContent = 'Dataset';
  const tableWrapper = document.createElement('div');
  tableWrapper.className = 'table-wrapper';
  const table = document.createElement('table');
  const thead = document.createElement('thead');
  thead.innerHTML = `
    <tr>
      <th>Label</th>
      <th>Ritual</th>
      <th>Trade</th>
      <th>Symbolism</th>
      <th>Hierarchy</th>
      <th>Diversity</th>
      <th>Multilinguality</th>
      <th>Hybridity</th>
      <th>NLIS</th>
      <th>CRM</th>
    </tr>`;
  let tbody = document.createElement('tbody');
  table.appendChild(thead);
  table.appendChild(tbody);
  tableWrapper.appendChild(table);
  tableSection.appendChild(tableHeading);
  tableSection.appendChild(tableWrapper);

  app.appendChild(header);
  app.appendChild(controls);
  app.appendChild(chartsSection);
  app.appendChild(tableSection);

  const charts = createCharts(distributionCanvas, scatterCanvas);

  let records: CulturalRecord[] = [];

  const update = (data: CulturalRecord[]) => {
    records = data;
    const enriched = enrichRecords(records);
    const newBody = createTable(enriched);
    tbody.replaceWith(newBody);
    tbody = newBody;
    charts.update(enriched);
    status.textContent = `${records.length} records loaded`;
  };

  fileInput.addEventListener('change', async () => {
    const [file] = Array.from(fileInput.files ?? []);
    if (!file) return;
    status.textContent = 'Parsing…';
    const parsed = await parseCsvFile(file);
    update(parsed);
  });

  sampleButton.addEventListener('click', async () => {
    status.textContent = 'Loading sample…';
    const parsed = await loadSample();
    update(parsed);
  });

  const sample = await loadSample();
  update(sample);
}

bootstrap();
