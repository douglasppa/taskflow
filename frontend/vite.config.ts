/// <reference types="vitest/globals" />
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    css: true,
    coverage: {
      reporter: ['text', 'html', 'lcov'],
      reportsDirectory: 'coverage',
      exclude: [
        'node_modules/',
        'dist/',
        'frontend/dist/',
        'frontend/public/',
        '**/__tests__/**',
        '**/*.test.tsx',
        '**/*.test.ts',
        '**/*.d.ts',
        'vite.config.ts',
        'src/types/',
        'src/assets/',
        'src/utils/version.ts',
        'src/main.tsx',
        'src/App.tsx',
        'src/routes.tsx',
        'eslint.config.js',
        'postcss.config.js',
        'tailwind.config.js',
      ],
    },
  },
});
