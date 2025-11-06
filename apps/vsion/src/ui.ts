import Chart from 'chart.js/auto';
import type { SimulationParams, SimulationResult, AgentState } from './sim';

export interface AppHandles {
  update(result: SimulationResult): void;
  setShareHandler(handler: () => void): void;
}

interface SliderConfig {
  key: keyof SimulationParams;
  label: string;
}

const sliders: SliderConfig[] = [
  { key: 'ritual', label: 'Ritual' },
  { key: 'trade', label: 'Trade' },
  { key: 'symbolism', label: 'Symbolism' },
  { key: 'hierarchy', label: 'Hierarchy' }
];

export function createApp(
  root: HTMLElement,
  initialParams: SimulationParams,
  onParamsChange: (params: SimulationParams) => void
): AppHandles {
  root.innerHTML = '';

  const container = document.createElement('div');
  container.id = 'app';

  const controls = document.createElement('section');
  controls.className = 'controls';

  const title = document.createElement('h1');
  title.textContent = 'vSION';
  controls.appendChild(title);

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Tune cultural pressures and watch the network evolve in real time. Use the share link to preserve your configuration.';
  controls.appendChild(subtitle);

  const sliderGroup = document.createElement('div');
  sliderGroup.className = 'slider-group';

  const params: SimulationParams = { ...initialParams };

  sliders.forEach((slider) => {
    const wrapper = document.createElement('label');
    wrapper.textContent = slider.label;
    const valueSpan = document.createElement('span');
    valueSpan.textContent = params[slider.key].toFixed(2);
    valueSpan.style.marginLeft = 'auto';
    valueSpan.style.fontVariantNumeric = 'tabular-nums';

    const input = document.createElement('input');
    input.type = 'range';
    input.min = '0';
    input.max = '1';
    input.step = '0.01';
    input.value = params[slider.key].toString();
    input.setAttribute('aria-label', `${slider.label} intensity`);

    input.addEventListener('input', () => {
      const value = Number.parseFloat(input.value);
      params[slider.key] = value;
      valueSpan.textContent = value.toFixed(2);
      onParamsChange({ ...params });
    });

    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.flexDirection = 'column';
    row.style.gap = '0.35rem';

    const headerRow = document.createElement('div');
    headerRow.style.display = 'flex';
    headerRow.style.alignItems = 'center';
    headerRow.style.gap = '0.75rem';

    const labelSpan = document.createElement('span');
    labelSpan.textContent = slider.label;

    headerRow.appendChild(labelSpan);
    headerRow.appendChild(valueSpan);
    row.appendChild(headerRow);
    row.appendChild(input);
    sliderGroup.appendChild(row);
  });

  controls.appendChild(sliderGroup);

  const shareButton = document.createElement('button');
  shareButton.className = 'share';
  shareButton.type = 'button';
  shareButton.textContent = 'Share configuration';
  controls.appendChild(shareButton);

  const visuals = document.createElement('section');
  visuals.className = 'visuals';

  const canvas = document.createElement('canvas');
  canvas.id = 'network';
  canvas.width = 720;
  canvas.height = 480;
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', 'Simulation network visualisation');

  const chartCanvas = document.createElement('canvas');
  chartCanvas.id = 'chart';
  chartCanvas.height = 260;

  visuals.appendChild(canvas);
  visuals.appendChild(chartCanvas);

  container.appendChild(controls);
  container.appendChild(visuals);
  root.appendChild(container);

  const chart = new Chart(chartCanvas, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        { label: 'Cohesion', data: [], borderColor: '#7f5af0', tension: 0.3 },
        { label: 'Creativity', data: [], borderColor: '#2cb1bc', tension: 0.3 },
        { label: 'Connectivity', data: [], borderColor: '#ffa94d', tension: 0.3 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { min: 0, max: 1 }
      },
      plugins: {
        legend: {
          labels: {
            color: '#e2e8f0'
          }
        }
      }
    }
  });

  const drawNetwork = (agents: AgentState[]) => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 40;

    const positions = agents.map((agent, index) => {
      const angle = (index / agents.length) * Math.PI * 2;
      const r = radius * (0.6 + agent.trade * 0.3);
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      return { agent, x, y };
    });

    ctx.globalAlpha = 0.18;
    ctx.strokeStyle = '#7f5af0';
    positions.forEach((source, index) => {
      positions.slice(index + 1).forEach((target) => {
        const weight = (source.agent.trade + target.agent.trade) / 2;
        const strength = Math.max(0.1, weight);
        ctx.lineWidth = strength * 2.2;
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        ctx.stroke();
      });
    });

    ctx.globalAlpha = 1;
    positions.forEach(({ agent, x, y }) => {
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, 28);
      const colour = symbolismColour(agent.symbolism);
      gradient.addColorStop(0, colour);
      gradient.addColorStop(1, '#0b1026');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(x, y, 14 + agent.hierarchy * 10, 0, Math.PI * 2);
      ctx.fill();
    });
  };

  const updateChart = (result: SimulationResult) => {
    chart.data.labels = result.history.map((entry) => entry.step.toString());
    chart.data.datasets[0].data = result.history.map((entry) => entry.cohesion);
    chart.data.datasets[1].data = result.history.map((entry) => entry.creativity);
    chart.data.datasets[2].data = result.history.map((entry) => entry.connectivity);
    chart.update();
  };

  const update = (result: SimulationResult) => {
    drawNetwork(result.agents);
    updateChart(result);
  };

  return {
    update,
    setShareHandler(handler: () => void) {
      shareButton.addEventListener('click', handler);
    }
  };
}

function symbolismColour(value: number): string {
  const hue = 260 + value * 40;
  return `hsl(${hue}, 80%, ${45 + value * 10}%)`;
}
