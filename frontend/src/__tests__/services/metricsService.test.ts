import { describe, it, vi, beforeEach, expect } from 'vitest';
import axios from 'axios';
import { sendMetric } from '../../services/metricsService';
import type { Metric } from 'web-vitals';

vi.mock('axios');

const mockedAxios = vi.mocked(axios, true);

describe('sendMetric', () => {
  const fakeMetric: Metric = {
    name: 'LCP',
    value: 1234.56,
    delta: 50,
    id: 'metric-id-123',
    rating: 'good',
    navigationType: 'navigate',
    entries: [],
  };

  beforeEach(() => {
    mockedAxios.post.mockReset();
    mockedAxios.post.mockResolvedValue({});
  });

  it('envia a métrica com os dados corretos', () => {
    sendMetric(fakeMetric);

    expect(mockedAxios.post).toHaveBeenCalledTimes(1);
    const [url, body] = mockedAxios.post.mock.calls[0] as [
      string,
      Metric & { timestamp: string },
    ];

    expect(url).toMatch(/\/api\/v1\/metrics$/);
    expect(body.name).toBe(fakeMetric.name);
  });

  it('não lança erro se o envio falhar', () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Erro simulado'));

    expect(() => sendMetric(fakeMetric)).not.toThrow();
  });
});
