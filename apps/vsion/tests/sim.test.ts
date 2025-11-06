import { describe, expect, it } from 'vitest';
import { simulate, type SimulationParams } from '../src/sim';

const BASE_PARAMS: SimulationParams = {
  ritual: 0.5,
  trade: 0.5,
  symbolism: 0.5,
  hierarchy: 0.5
};

describe('simulate', () => {
  it('produces deterministic results for a given seed', () => {
    const first = simulate(BASE_PARAMS, { seed: 123, steps: 10, agents: 6 });
    const second = simulate(BASE_PARAMS, { seed: 123, steps: 10, agents: 6 });
    expect(second.history).toStrictEqual(first.history);
    expect(second.agents).toStrictEqual(first.agents);
  });

  it('responds to changes in cultural parameters', () => {
    const ritualLow = simulate({ ...BASE_PARAMS, ritual: 0.2 }, { seed: 5, steps: 8, agents: 6 });
    const ritualHigh = simulate({ ...BASE_PARAMS, ritual: 0.9 }, { seed: 5, steps: 8, agents: 6 });
    const finalLow = ritualLow.history.at(-1)?.creativity ?? 0;
    const finalHigh = ritualHigh.history.at(-1)?.creativity ?? 0;
    expect(finalHigh).toBeGreaterThan(finalLow);
  });
});
