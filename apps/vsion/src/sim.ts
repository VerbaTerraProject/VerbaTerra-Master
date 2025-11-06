export interface SimulationParams {
  ritual: number;
  trade: number;
  symbolism: number;
  hierarchy: number;
}

export interface AgentState {
  id: number;
  ritual: number;
  trade: number;
  symbolism: number;
  hierarchy: number;
  cognition: number;
  languageComplexity: number;
}

export interface HistoryPoint {
  step: number;
  cohesion: number;
  creativity: number;
  connectivity: number;
}

export interface SimulationResult {
  agents: AgentState[];
  history: HistoryPoint[];
}

type RNG = () => number;

function clamp(value: number, min = 0, max = 1): number {
  return Math.min(max, Math.max(min, value));
}

function createRng(seed: number): RNG {
  let value = seed % 2147483647;
  if (value <= 0) value += 2147483646;
  return () => {
    value = (value * 16807) % 2147483647;
    return (value - 1) / 2147483646;
  };
}

function createAgents(count: number, params: SimulationParams, rng: RNG): AgentState[] {
  return Array.from({ length: count }, (_, index) => {
    const noise = () => (rng() - 0.5) * 0.2;
    return {
      id: index,
      ritual: clamp(params.ritual + noise()),
      trade: clamp(params.trade + noise()),
      symbolism: clamp(params.symbolism + noise()),
      hierarchy: clamp(params.hierarchy + noise()),
      cognition: clamp(0.4 + params.symbolism * 0.4 + rng() * 0.2),
      languageComplexity: clamp(0.3 + params.ritual * 0.3 + params.symbolism * 0.2 + rng() * 0.2)
    };
  });
}

function updateAgent(agent: AgentState, params: SimulationParams, rng: RNG): AgentState {
  const tradeInfluence = params.trade * 0.2;
  const ritualInfluence = params.ritual * 0.15;
  const hierarchyDrift = (params.hierarchy - agent.hierarchy) * 0.1;
  const symbolismGain = (params.symbolism - agent.symbolism) * 0.12;

  const newRitual = clamp(agent.ritual + ritualInfluence - agent.trade * 0.05 + (rng() - 0.5) * 0.05);
  const newTrade = clamp(agent.trade + tradeInfluence - agent.hierarchy * 0.04 + (rng() - 0.5) * 0.04);
  const newSymbolism = clamp(agent.symbolism + symbolismGain + newRitual * 0.03 + (rng() - 0.5) * 0.04);
  const newHierarchy = clamp(agent.hierarchy + hierarchyDrift + newTrade * 0.02 + (rng() - 0.5) * 0.03);

  const cognition = clamp(agent.cognition + (newSymbolism - 0.5) * 0.08 + (rng() - 0.5) * 0.05);
  const languageComplexity = clamp(
    agent.languageComplexity + (newRitual + newSymbolism) * 0.04 - newHierarchy * 0.03 + (rng() - 0.5) * 0.05
  );

  return {
    ...agent,
    ritual: newRitual,
    trade: newTrade,
    symbolism: newSymbolism,
    hierarchy: newHierarchy,
    cognition,
    languageComplexity
  };
}

function aggregateHistory(step: number, agents: AgentState[]): HistoryPoint {
  const cohesion = average(agents.map((agent) => 1 - Math.abs(agent.ritual - agent.hierarchy)));
  const creativity = average(agents.map((agent) => agent.cognition + agent.languageComplexity)) / 2;
  const connectivity = average(agents.map((agent) => agent.trade + agent.symbolism)) / 2;
  return {
    step,
    cohesion: Number(cohesion.toFixed(3)),
    creativity: Number(creativity.toFixed(3)),
    connectivity: Number(connectivity.toFixed(3))
  };
}

function average(values: number[]): number {
  if (!values.length) return 0;
  return values.reduce((acc, value) => acc + value, 0) / values.length;
}

export function simulate(
  params: SimulationParams,
  options: { steps?: number; agents?: number; seed?: number } = {}
): SimulationResult {
  const steps = options.steps ?? 48;
  const agentCount = options.agents ?? 24;
  const seed = options.seed ?? 1;
  const rng = createRng(seed);

  let agents = createAgents(agentCount, params, rng);
  const history: HistoryPoint[] = [];

  for (let step = 0; step < steps; step += 1) {
    agents = agents.map((agent) => updateAgent(agent, params, rng));
    history.push(aggregateHistory(step, agents));
  }

  return {
    agents,
    history
  };
}
