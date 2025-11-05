# Metrics — NLIS & CRM

**NLIS (Neuro‑Linguistic Integration Score)**  
Inputs: `lexical_diversity`, `syntax_complexity`, plus normalized cultural drivers.  
Heuristic blend: language structure (60%) + cultural context (40%).  
Output in [0, 1] after normalization.

**CRM (Cultural Resilience Metric)**  
Inputs: `ritual`, `trade`, `symbolism`, `hierarchy`.  
Promotes trade/symbolism, penalizes hierarchy extremes, rewards ritual stability.
