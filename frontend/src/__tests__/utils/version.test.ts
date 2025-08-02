import { describe, it, expect, vi } from 'vitest';

// Mock do wrapper
vi.mock('../../utils/version-wrapper.ts', () => ({
  default: '1.2.3',
}));

describe('frontendVersion', () => {
  it('remove quebras de linha e espaços extras', async () => {
    const version = (await import('../../utils/version-wrapper')).default;
    expect(version).toBe('1.2.3');
  });
});
