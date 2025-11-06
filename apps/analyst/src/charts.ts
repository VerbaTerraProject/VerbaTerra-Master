import Chart from 'chart.js/auto';
import type { MetricRecord } from './metrics';

export interface ChartHandles {
  update(records: MetricRecord[]): void;
}

export function createCharts(distributionCanvas: HTMLCanvasElement, scatterCanvas: HTMLCanvasElement): ChartHandles {
  const distributionChart = new Chart(distributionCanvas, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        {
          label: 'NLIS',
          data: [],
          backgroundColor: 'rgba(37, 99, 235, 0.55)'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { min: 0, max: 1 }
      }
    }
  });

  const scatterChart = new Chart(scatterCanvas, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'NLIS vs CRM',
          data: [],
          backgroundColor: 'rgba(16, 185, 129, 0.7)'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: 'NLIS' },
          min: 0,
          max: 1
        },
        y: {
          title: { display: true, text: 'CRM' },
          min: 0,
          max: 1
        }
      }
    }
  });

  return {
    update(records: MetricRecord[]) {
      const sorted = [...records].sort((a, b) => b.nlis - a.nlis);
      distributionChart.data.labels = sorted.map((record) => record.label);
      distributionChart.data.datasets[0].data = sorted.map((record) => record.nlis);
      distributionChart.update();

      scatterChart.data.datasets[0].data = records.map((record) => ({ x: record.nlis, y: record.crm }));
      scatterChart.update();
    }
  };
}
