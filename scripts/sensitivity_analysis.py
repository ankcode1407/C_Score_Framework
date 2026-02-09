"""
TASK 3: NORMALIZED SENSITIVITY ANALYSIS
Re-run full sensitivity analysis with normalized [0,100] formula
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# --- 1. DYNAMIC PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIS_DIR = os.path.join(BASE_DIR, 'visualizations')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Create directories if they don't exist
for d in [VIS_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

print("="*80)
print("TASK 3: NORMALIZED SENSITIVITY ANALYSIS")
print("Testing Robustness with Bounded [0,100] Scoring")
print("="*80)

# --- 2. LOAD DATA ---
input_path = os.path.join(DATA_DIR, 'morgan_stanley_claims_dataset.csv')
if not os.path.exists(input_path):
    print(f"[!] CRITICAL ERROR: Dataset not found at {input_path}")
    exit()

df = pd.read_csv(input_path)

# Normalization constant (Fixed per paper definition)
W_MAX = 1.2

# Penalty configuration
PENALTY_POINTS = {'ScopeOmission': 15}
detected_tactics = {'ScopeOmission': 1}

def clamp(x, min_val=0.0, max_val=1.0):
    """Clamp value to [min_val, max_val]"""
    return max(min_val, min(max_val, x))

def calculate_normalized_c_score_scenario(claims_df, weights, detected_tactics=None):
    """
    Calculate normalized C_Score for a given weight scenario
    """
    # Effective denominator
    n_nc = (claims_df['category'] == 'NonClaim').sum()
    n_total = len(claims_df)
    
    if n_nc <= 0.5 * n_total:
        n_eff = n_total - n_nc
    else:
        n_eff = 0.5 * n_total
    
    # Weighted sum
    claims_df_temp = claims_df.copy()
    claims_df_temp['weight_applied'] = claims_df_temp['category'].map(weights)
    weighted_sum = claims_df_temp['weight_applied'].sum()
    
    # Raw average
    raw_avg = weighted_sum / n_eff
    
    # [MODIFIED] Normalize by fixed global W_MAX (1.2)
    # This ensures consistency. If a scenario uses higher weights (e.g., 1.5),
    # the score should reflect that increase rather than being normalized away.
    normalized = raw_avg / W_MAX
    
    # Penalty fraction
    penalty_frac = 0.0
    if detected_tactics:
        for tactic, count in detected_tactics.items():
            if count > 0:
                penalty_points = PENALTY_POINTS.get(tactic, 0)
                penalty_frac += penalty_points / 100.0
    
    # Final score
    clamped = clamp(normalized - penalty_frac, 0.0, 1.0)
    final_score = 100.0 * clamped
    
    return {
        'weighted_sum': float(weighted_sum),
        'raw_avg': float(raw_avg),
        'w_max': float(W_MAX),
        'normalized': float(normalized),
        'penalty_frac': float(penalty_frac),
        'clamped': float(clamped),
        'final_score': float(final_score)
    }

# Define weight scenarios
scenarios = {
    "Conservative": {
        "QuantitativeTarget": 1.0,
        "VerifiedClaim": 1.0,
        "PeripheralClaim": 0.2,
        "VagueTarget": -0.5,
        "AmbiguousBaseline": -0.5,
        "OffsetsOnly": -0.3,
        "NonClaim": 0.0,
        "rationale": "Reduced penalties and rewards (±17-33% from baseline)"
    },
    "Current (Theoretical)": {
        "QuantitativeTarget": 1.2,
        "VerifiedClaim": 1.2,
        "PeripheralClaim": 0.3,
        "VagueTarget": -0.8,
        "AmbiguousBaseline": -0.8,
        "OffsetsOnly": -0.5,
        "NonClaim": 0.0,
        "rationale": "Theoretically-derived weights from paper"
    },
    "Aggressive": {
        "QuantitativeTarget": 1.5,
        "VerifiedClaim": 1.5,
        "PeripheralClaim": 0.4,
        "VagueTarget": -1.0,
        "AmbiguousBaseline": -1.0,
        "OffsetsOnly": -0.7,
        "NonClaim": 0.0,
        "rationale": "Increased penalties and rewards (+25% from baseline)"
    },
    "Empirically-Calibrated": {
        "QuantitativeTarget": 1.3,
        "VerifiedClaim": 1.1,
        "PeripheralClaim": 0.25,
        "VagueTarget": -0.9,
        "AmbiguousBaseline": -0.7,
        "OffsetsOnly": -0.6,
        "NonClaim": 0.0,
        "rationale": "Based on SEC enforcement severity analysis"
    },
    "Equal Weights": {
        "QuantitativeTarget": 1.0,
        "VerifiedClaim": 1.0,
        "PeripheralClaim": 1.0,
        "VagueTarget": -1.0,
        "AmbiguousBaseline": -1.0,
        "OffsetsOnly": -1.0,
        "NonClaim": 0.0,
        "rationale": "Naive baseline - all positive equal, all negative equal"
    }
}

print("\n" + "="*80)
print("SCENARIO RESULTS (NORMALIZED)")
print("="*80)

results = {}

for scenario_name, weights in scenarios.items():
    result = calculate_normalized_c_score_scenario(df, weights, detected_tactics)
    results[scenario_name] = result
    
    print(f"\n{scenario_name}:")
    print(f"  Weighted Sum:        {result['weighted_sum']:.2f}")
    print(f"  Normalized:          {result['normalized']:.4f}")
    print(f"  Final C_Score:       {result['final_score']:.2f}")
    print(f"  Rationale: {weights.get('rationale', '')}")

# Statistical summary
scores = [r['final_score'] for r in results.values()]

print("\n" + "="*80)
print("ROBUSTNESS STATISTICS")
print("="*80)

mean_score = np.mean(scores)
std_score = np.std(scores)
cv = (std_score / mean_score) * 100

print(f"\nC_Score Range:        [{min(scores):.2f}, {max(scores):.2f}]")
print(f"Spread:               {max(scores) - min(scores):.2f} points")
print(f"Mean:                 {mean_score:.2f}")
print(f"Standard Deviation:   {std_score:.2f}")
print(f"Coefficient of Variation: {cv:.1f}%")

# Check if any score exceeds bounds
print(f"\n" + "="*80)
print("BOUNDS CHECK")
print("="*80)

exceeds_100 = [name for name, r in results.items() if r['final_score'] > 100]
below_0 = [name for name, r in results.items() if r['final_score'] < 0]

if exceeds_100:
    print(f"⚠ VIOLATION: Scenarios exceeding 100: {exceeds_100}")
else:
    print(f"✓ No scenarios exceed 100")

print(f"\n✓ All scores in [{min(scores):.2f}, {max(scores):.2f}] ⊂ [0, 100]")

# Classification stability
print("\n" + "="*80)
print("CLASSIFICATION TIER STABILITY")
print("="*80)

TIERS = {
    'Exceptional Credibility': (80, 100),
    'High Credibility': (60, 80),
    'Moderate Credibility': (40, 60),
    'Low Credibility': (20, 40),
    'Very Low Credibility': (0, 20)
}

def classify_score(score):
    for tier, (low, high) in TIERS.items():
        if low <= score < high or (tier == 'Exceptional Credibility' and score == 100):
            return tier
    return 'Very Low Credibility'

classifications = {}
for scenario, result in results.items():
    tier = classify_score(result['final_score'])
    classifications[scenario] = tier
    print(f"{scenario:30s}: {result['final_score']:6.2f} → {tier}")

unique_tiers = set(classifications.values())
print(f"\nUnique tiers: {len(unique_tiers)}")
print(f"Tiers: {', '.join(sorted(unique_tiers))}")

# Section-level rank order stability
print("\n" + "="*80)
print("SECTION RANK ORDER STABILITY")
print("="*80)

for scenario_name, weights in scenarios.items():
    section_scores = {}
    for section in df['section'].unique():
        section_df = df[df['section'] == section]
        
        # Apply penalty only to Climate
        if section == 'Climate':
            section_tactics = detected_tactics
        else:
            section_tactics = {}
        
        result = calculate_normalized_c_score_scenario(section_df, weights, section_tactics)
        section_scores[section] = result['final_score']
    
    ranked = sorted(section_scores.items(), key=lambda x: x[1])
    print(f"\n{scenario_name}:")
    for rank, (section, score) in enumerate(ranked, 1):
        print(f"  #{rank}: {section:20s} ({score:6.2f})")

# Check rank order consistency
print("\n" + "="*80)
print("RANK ORDER CONSISTENCY CHECK")
print("="*80)

rank_orders = []
for scenario_name, weights in scenarios.items():
    section_scores = {}
    for section in df['section'].unique():
        section_df = df[df['section'] == section]
        
        if section == 'Climate':
            section_tactics = detected_tactics
        else:
            section_tactics = {}
        
        result = calculate_normalized_c_score_scenario(section_df, weights, section_tactics)
        section_scores[section] = result['final_score']
    
    ranked_sections = [s[0] for s in sorted(section_scores.items(), key=lambda x: x[1])]
    rank_orders.append(ranked_sections)

# Check if all rank orders are identical
first_order = rank_orders[0]
all_identical = all(order == first_order for order in rank_orders)

if all_identical:
    print(f"✓ RANK ORDER PERFECTLY STABLE across all scenarios")
    print(f"  Consistent ordering: {' < '.join(first_order)}")
else:
    print(f"⚠ RANK ORDER VARIES across scenarios")

# Save results
sensitivity_results = {
    'scenarios': results,
    'statistics': {
        'mean': float(mean_score),
        'std': float(std_score),
        'cv': float(cv),
        'min': float(min(scores)),
        'max': float(max(scores)),
        'range': float(max(scores) - min(scores))
    },
    'rank_order_stability': {
        'stable': all_identical,
        'consistent_order': first_order if all_identical else None
    }
}

json_out = os.path.join(DOCS_DIR, 'normalized_sensitivity_results.json')
with open(json_out, 'w') as f:
    json.dump(sensitivity_results, f, indent=2)

print(f"\n✓ Results saved to: {json_out}")

# VISUALIZATION 1: Sensitivity Plot
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

fig, ax = plt.subplots(figsize=(12, 6))
scenario_names = list(results.keys())
c_scores = [results[s]['final_score'] for s in scenario_names]

colors = ['#95a5a6', '#3498db', '#e74c3c', '#2ecc71', '#f39c12']
bars = ax.bar(range(len(scenario_names)), c_scores, color=colors, alpha=0.8)

ax.set_xticks(range(len(scenario_names)))
ax.set_xticklabels(scenario_names, rotation=15, ha='right')
ax.set_ylabel('Normalized C_Score', fontsize=12, fontweight='bold')
ax.set_title('Normalized Sensitivity Analysis: C_Score Under Different Weight Scenarios', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylim([0, 105])

# Add tier thresholds
ax.axhline(y=80, color='green', linestyle='--', linewidth=1.5, alpha=0.6, label='Exceptional (80+)')
ax.axhline(y=60, color='orange', linestyle='--', linewidth=1.5, alpha=0.6, label='High (60+)')
ax.axhline(y=40, color='yellow', linestyle='--', linewidth=1.5, alpha=0.6, label='Moderate (40+)')
ax.axhline(y=20, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='Low (20+)')
ax.grid(axis='y', alpha=0.3)
ax.legend(loc='upper left', fontsize=9)

# Add value labels
for i, (bar, score) in enumerate(zip(bars, c_scores)):
    ax.text(i, score + 2, f'{score:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    tier = classify_score(score)
    tier_short = tier.split()[0]  # "Moderate" from "Moderate Credibility"
    ax.text(i, score - 5, tier_short, ha='center', va='top', fontsize=8, style='italic', alpha=0.7)

# Add variation range shading
min_score_val = min(c_scores)
max_score_val = max(c_scores)
ax.axhspan(min_score_val, max_score_val, alpha=0.1, color='blue', 
           label=f'Variation Range ({max_score_val-min_score_val:.1f} pts)')

plt.tight_layout()
save_path_14 = os.path.join(VIS_DIR, '14_normalized_sensitivity.png')
plt.savefig(save_path_14, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {save_path_14}")

# VISUALIZATION 2: Section scores across scenarios
fig, ax = plt.subplots(figsize=(14, 7))

sections = df['section'].unique()
x = np.arange(len(scenario_names))
width = 0.25

for i, section in enumerate(sections):
    section_scores_list = []
    for scenario_name, weights in scenarios.items():
        section_df = df[df['section'] == section]
        
        if section == 'Climate':
            section_tactics = detected_tactics
        else:
            section_tactics = {}
        
        result = calculate_normalized_c_score_scenario(section_df, weights, section_tactics)
        section_scores_list.append(result['final_score'])
    
    ax.bar(x + i*width, section_scores_list, width, label=section, alpha=0.8)

ax.set_xlabel('Weight Scenario', fontsize=12, fontweight='bold')
ax.set_ylabel('Normalized Section C_Score', fontsize=12, fontweight='bold')
ax.set_title('Section-Level Normalized Sensitivity: Rank Order Stability Test', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x + width)
ax.set_xticklabels(scenario_names, rotation=15, ha='right')
ax.set_ylim([0, 105])
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=0, color='black', linewidth=0.8)

plt.tight_layout()
save_path_15 = os.path.join(VIS_DIR, '15_normalized_section_sensitivity.png')
plt.savefig(save_path_15, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {save_path_15}")

print("\n" + "="*80)
print("NORMALIZED SENSITIVITY ANALYSIS COMPLETE")
print("="*80)

print(f"\n📊 SUMMARY:")
print(f"   Mean C_Score:                 {mean_score:.2f}")
print(f"   Standard Deviation:           {std_score:.2f}")
print(f"   Coefficient of Variation:     {cv:.1f}%")
print(f"   Score Range:                  [{min(scores):.2f}, {max(scores):.2f}]")
print(f"   All scores within [0,100]:    ✓")
print(f"   Rank order stable:            {'✓' if all_identical else '✗'}")
print(f"   Tier distribution:            {len(unique_tiers)} unique tiers")