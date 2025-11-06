import { describe, expect, it } from 'vitest';
import { calculateCRM, calculateNLIS, enrichRecords, type CulturalRecord } from '../src/metrics';

const BASE_RECORD: CulturalRecord = {
  id: 1,
  label: 'Test',
  ritual: 0.5,
  trade: 0.5,
  symbolism: 0.5,
  hierarchy: 0.5,
  diversity: 0.5,
  multilinguality: 0.5,
  hybridity: 0.5
};

describe('metrics', () => {
  it('computes NLIS using default weights', () => {
    const value = calculateNLIS(BASE_RECORD);
    expect(value).toBeCloseTo(0.5, 2);
  });

  it('computes CRM using default coefficients', () => {
    const value = calculateCRM(BASE_RECORD);
    expect(value).toBeCloseTo(0.5, 2);
  });

  it('enrichRecords adds metrics and keeps cultural data', () => {
    const enriched = enrichRecords([BASE_RECORD]);
    expect(enriched).toHaveLength(1);
    expect(enriched[0].nlis).toBeGreaterThan(0);
    expect(enriched[0].crm).toBeGreaterThan(0);
    expect(enriched[0].label).toBe('Test');
  });
});
