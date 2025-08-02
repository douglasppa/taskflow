import type { Metric } from 'web-vitals';
import axios from 'axios';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const METRICS_PATH = import.meta.env.VITE_API_METRICS_PATH || '/api/v1/metrics';
const METRICS_URL = `${BASE_URL}${METRICS_PATH}`;

const route = window.location.pathname;
const userAgent = navigator.userAgent;
let browser = 'Unknown';

if (userAgent.includes('Chrome')) {
  browser = 'Chrome';
} else if (userAgent.includes('Firefox')) {
  browser = 'Firefox';
} else if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) {
  browser = 'Safari';
} else if (userAgent.includes('Edge')) {
  browser = 'Edge';
}

export function sendMetric(metric: Metric) {
  axios
    .post(METRICS_URL, {
      name: metric.name,
      value: metric.value,
      id: metric.id,
      delta: metric.delta,
      rating: metric.rating,
      navigationType: metric.navigationType,
      timestamp: new Date().toISOString(),
      route: route,
      browser: browser,
    })
    .catch((error) => {
      console.error('Erro ao enviar métrica:', error);
    });
}
