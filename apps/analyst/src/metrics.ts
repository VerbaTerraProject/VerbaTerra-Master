export interface CulturalRecord {
  id: number;
  label: string;
  ritual: number;
  trade: number;
  symbolism: number;
  hierarchy: number;
  diversity: number;
  multilinguality: number;
  hybridity: number;
}

export interface MetricConfig {
  nlisWeights?: {
    ritual: number;
    trade: number;
    symbolism: number;
    hierarchy: number;
  };
  crmCoefficients?: {
    diversity: number;
    multilinguality: number;
    hybridity: number;
  };
}

export interface MetricRecord extends CulturalRecord {
  nlis: number;
  crm: number;
}

const DEFAULT_NLIS = {
  ritual: 0.3,
  trade: 0.25,
  symbolism: 0.25,
  hierarchy: 0.2
} as const;

const DEFAULT_CRM = {
  diversity: 0.4,
  multilinguality: 0.35,
  hybridity: 0.25
} as const;

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value));
}

export function calculateNLIS(record: CulturalRecord, weights = DEFAULT_NLIS): number {
  const total =
    record.ritual * weights.ritual +
    record.trade * weights.trade +
    record.symbolism * weights.symbolism +
    record.hierarchy * weights.hierarchy;
  return Number(clamp01(total).toFixed(3));
}

export function calculateCRM(record: CulturalRecord, coefficients = DEFAULT_CRM): number {
  const total =
    record.diversity * coefficients.diversity +
    record.multilinguality * coefficients.multilinguality +
    record.hybridity * coefficients.hybridity;
  return Number(clamp01(total).toFixed(3));
}

export function enrichRecords(records: CulturalRecord[], config: MetricConfig = {}): MetricRecord[] {
  return records.map((record) => ({
    ...record,
    nlis: calculateNLIS(record, config.nlisWeights ?? DEFAULT_NLIS),
    crm: calculateCRM(record, config.crmCoefficients ?? DEFAULT_CRM)
  }));
}
