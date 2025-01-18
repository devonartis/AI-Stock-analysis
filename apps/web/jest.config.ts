import type { Config } from 'jest';
import nextJest from 'next/jest';

const createJestConfig = nextJest({
  dir: './',
});

const config: Config = {
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  // Only test our custom components
  testMatch: ['**/__tests__/**/*.[jt]s?(x)'],
  // Don't collect coverage for everything
  collectCoverage: false,
};

export default createJestConfig(config);
