import { describe, it, expect, vi } from 'vitest';

// ✅ Mock explícito do módulo ESM
vi.mock('web-vitals', () => ({
  onCLS: vi.fn(),
  onINP: vi.fn(),
  onLCP: vi.fn(),
  onTTFB: vi.fn(),
  onFCP: vi.fn(),
}));

import { onCLS, onINP, onLCP, onTTFB, onFCP } from 'web-vitals';

import { reportWebVitals } from '../../utils/reportWebVitals';

describe('reportWebVitals', () => {
  const mockCallback = vi.fn();

  it('chama todas as funções do web-vitals com o callback', () => {
    reportWebVitals(mockCallback);

    expect(onCLS).toHaveBeenCalledWith(mockCallback);
    expect(onINP).toHaveBeenCalledWith(mockCallback);
    expect(onLCP).toHaveBeenCalledWith(mockCallback);
    expect(onTTFB).toHaveBeenCalledWith(mockCallback);
    expect(onFCP).toHaveBeenCalledWith(mockCallback);
  });
});
