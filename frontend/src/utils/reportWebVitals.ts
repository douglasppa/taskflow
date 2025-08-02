import { onCLS, onINP, onLCP, onTTFB, onFCP, type Metric } from 'web-vitals';

export function reportWebVitals(onReport: (metric: Metric) => void): void {
  onCLS(onReport);
  onINP(onReport);
  onLCP(onReport);
  onTTFB(onReport);
  onFCP(onReport);
}
