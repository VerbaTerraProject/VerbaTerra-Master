import Papa from 'papaparse';
import type { CulturalRecord } from './metrics';

interface ColumnMap {
  label: string;
  ritual: string;
  trade: string;
  symbolism: string;
  hierarchy: string;
  diversity: string;
  multilinguality: string;
  hybridity: string;
}

const COLUMN_ALIASES: Record<keyof ColumnMap, string[]> = {
  label: ['label', 'name', 'group', 'community'],
  ritual: ['ritual'],
  trade: ['trade', 'commerce'],
  symbolism: ['symbolism', 'symbolic'],
  hierarchy: ['hierarchy', 'stratification'],
  diversity: ['diversity'],
  multilinguality: ['multilinguality', 'languages'],
  hybridity: ['hybridity', 'blending']
};

function findColumn(columns: string[], aliases: string[]): string {
  const lower = columns.map((column) => column.toLowerCase());
  for (const alias of aliases) {
    const index = lower.indexOf(alias.toLowerCase());
    if (index >= 0) {
      return columns[index];
    }
  }
  return aliases[0];
}

function inferColumnMap(columns: string[]): ColumnMap {
  return {
    label: findColumn(columns, COLUMN_ALIASES.label),
    ritual: findColumn(columns, COLUMN_ALIASES.ritual),
    trade: findColumn(columns, COLUMN_ALIASES.trade),
    symbolism: findColumn(columns, COLUMN_ALIASES.symbolism),
    hierarchy: findColumn(columns, COLUMN_ALIASES.hierarchy),
    diversity: findColumn(columns, COLUMN_ALIASES.diversity),
    multilinguality: findColumn(columns, COLUMN_ALIASES.multilinguality),
    hybridity: findColumn(columns, COLUMN_ALIASES.hybridity)
  };
}

function toNumber(value: unknown): number {
  const numeric = typeof value === 'number' ? value : Number.parseFloat(String(value ?? '0'));
  if (Number.isNaN(numeric)) return 0;
  return Math.min(1, Math.max(0, numeric));
}

export function parseCsvText(text: string): CulturalRecord[] {
  const result = Papa.parse<Record<string, unknown>>(text, {
    header: true,
    skipEmptyLines: 'greedy'
  });

  if (!result.meta.fields || !result.meta.fields.length) {
    return [];
  }

  const map = inferColumnMap(result.meta.fields);

  return result.data
    .filter(Boolean)
    .map((row, index) => ({
      id: index,
      label: String(row[map.label] ?? `Record ${index + 1}`),
      ritual: toNumber(row[map.ritual]),
      trade: toNumber(row[map.trade]),
      symbolism: toNumber(row[map.symbolism]),
      hierarchy: toNumber(row[map.hierarchy]),
      diversity: toNumber(row[map.diversity]),
      multilinguality: toNumber(row[map.multilinguality]),
      hybridity: toNumber(row[map.hybridity])
    }));
}

export async function parseCsvFile(file: File): Promise<CulturalRecord[]> {
  const text = await file.text();
  return parseCsvText(text);
}
