export interface RuleWeights {
  ritual: number;
  trade: number;
  symbolism: number;
  hierarchy: number;
}

export interface LexemeResult {
  original: string;
  transformed: string;
  rulesApplied: string[];
  culturalImprint: number;
}

type RNG = () => number;

const BORROW_SUFFIXES = ['-ari', '-esh', '-uno', '-vai'];
const COMPOUND_LINKERS = ['-na-', '-ri-', '-su-'];
const VOWEL_SHIFTS: Record<string, string> = {
  a: 'e',
  e: 'i',
  i: 'a',
  o: 'u',
  u: 'o'
};

function createRng(seed: number): RNG {
  let value = seed % 2147483647;
  if (value <= 0) value += 2147483646;
  return () => {
    value = (value * 16807) % 2147483647;
    return (value - 1) / 2147483646;
  };
}

function borrowing(word: string, weight: number, rng: RNG, applied: string[]): string {
  if (weight < 0.2) return word;
  const suffixIndex = Math.floor(rng() * BORROW_SUFFIXES.length);
  const suffix = BORROW_SUFFIXES[suffixIndex];
  applied.push('borrowing');
  return word + suffix;
}

function compounding(word: string, partner: string, weight: number, rng: RNG, applied: string[]): string {
  if (weight < 0.35) return word;
  const linker = COMPOUND_LINKERS[Math.floor(rng() * COMPOUND_LINKERS.length)];
  applied.push('compounding');
  return `${partner}${linker}${word}`;
}

function semanticShift(word: string, weight: number, applied: string[]): string {
  if (weight < 0.25) return word;
  const characters = word.split('');
  const shifted = characters
    .map((char, index) => {
      if (/^[aeiou]$/i.test(char) && index % 2 === 0) {
        const key = char.toLowerCase();
        const replacement = VOWEL_SHIFTS[key];
        return char === char.toLowerCase() ? replacement : replacement.toUpperCase();
      }
      return char;
    })
    .join('');
  applied.push('shift');
  return shifted;
}

export function evolveLexicon(words: string[], weights: RuleWeights, seed = 1): LexemeResult[] {
  const rng = createRng(seed);
  return words.filter((word) => word.trim().length > 0).map((word, index, list) => {
    const applied: string[] = [];
    const trimmed = word.trim();
    const partner = list[(index + 1) % list.length]?.trim() ?? trimmed;

    let current = trimmed;
    current = borrowing(current, weights.trade, rng, applied);
    current = compounding(current, partner, weights.ritual, rng, applied);
    current = semanticShift(current, (weights.symbolism + weights.hierarchy) / 2, applied);

    const imprint = Number(
      (
        weights.ritual * 0.25 +
        weights.trade * 0.25 +
        weights.symbolism * 0.3 +
        weights.hierarchy * 0.2 +
        applied.length * 0.05
      ).toFixed(2)
    );

    return {
      original: trimmed,
      transformed: current,
      rulesApplied: applied,
      culturalImprint: Math.min(1, imprint)
    };
  });
}
