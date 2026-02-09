"""
FILE: c_score_calculator.py
AUTHOR: Shaurya Mishra (Amity University)
PURPOSE: Empirical Validation of C_Score using Morgan Stanley 2023 Data.
         Generates Figures 01–06.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
import os

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIS_DIR = os.path.join(BASE_DIR, 'visualizations')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Create directories if they don't exist
for d in [VIS_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def as_fraction(value):
    """
    Ensures penalties are treated as fractions.
    Example: 15 -> 0.15 ; 0.15 -> 0.15
    """
    v = float(value)
    return v / 100.0 if v > 1.0 else v


def main():
    print("=" * 80)
    print("C_SCORE FRAMEWORK: MAIN CALCULATOR")
    print("=" * 80)

    # --- LOAD DATA ---
    data_path = os.path.join(DATA_DIR, 'morgan_stanley_claims_dataset.csv')
    if not os.path.exists(data_path):
        print(f"[!] ERROR: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    print(f"[+] Loaded {len(df)} claims from {os.path.basename(data_path)}")

    # --- 1. ANALYSIS & SCORING ---

    # Weighted Sum
    total_weighted_sum = df['weight'].sum()
    n_total = len(df)

    # Adaptive Denominator (Eq. 2)
    n_nc = (df['category'] == 'NonClaim').sum()
    if n_nc <= 0.5 * n_total:
        n_eff = n_total - n_nc
    else:
        n_eff = int(0.5 * n_total)

    # --- PENALTIES (fractions, not integers) ---
    tactic_penalties = {
        'ScopeOmission': 0.15,
        'IntensityTricks': 0.10,
        'SelectiveDisclosure': 0.12,
        'BaselineManipulation': 0.08,
        'WeakTargets': 0.11,
        'OffsetsOnly': 0.05
    }

    penalty_sum = 0.0
    tactic_counts = Counter()

    if 'tactic_flags' in df.columns:
        for flags in df['tactic_flags'].dropna():
            if isinstance(flags, str) and flags.strip():
                for flag in flags.split(','):
                    f = flag.strip()
                    if f in tactic_penalties:
                        tactic_counts[f] += 1
                        penalty_sum += as_fraction(tactic_penalties[f])

    # --- FINAL C_SCORE ---
    avg_fraction = total_weighted_sum / n_eff
    raw_score = 100 * (avg_fraction - penalty_sum)
    final_c_score = max(0.0, min(100.0, raw_score))

    print(f"\nRESULTS:")
    print(f"  Weighted Sum:      {total_weighted_sum:.2f}")
    print(f"  n_total / n_eff:   {n_total} / {n_eff}")
    print(f"  Avg Fraction:      {avg_fraction:.4f}")
    print(f"  Penalty Sum:       {penalty_sum:.4f} ({dict(tactic_counts)})")
    print(f"  Final C_Score:     {final_c_score:.2f}")

    # --- 2. GENERATE VISUALIZATIONS ---

    # Fig 01: Category Distribution
    plt.figure(figsize=(10, 6))
    counts = df['category'].value_counts()
    counts.plot(kind='bar', color='steelblue', edgecolor='black')
    plt.title('Figure 1: Claim Category Distribution (Morgan Stanley 2023)', fontsize=12, fontweight='bold')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, '01_category_distribution.png'), dpi=300)
    print("  [+] Saved 01_category_distribution.png")

    # Fig 02: Weight Contribution
    plt.figure(figsize=(10, 6))
    w_contrib = df.groupby('category')['weight'].sum().sort_values(ascending=False)
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in w_contrib.values]
    w_contrib.plot(kind='bar', color=colors, edgecolor='black')
    plt.title('Figure 2: Weight Contribution by Category', fontsize=12, fontweight='bold')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, '02_weight_contribution.png'), dpi=300)
    print("  [+] Saved 02_weight_contribution.png")

    # Fig 03: Section Comparison (adaptive denominator per section)
    plt.figure(figsize=(8, 5))

    def section_score(x):
        n = len(x)
        n_nc_sec = (x['category'] == 'NonClaim').sum()
        if n_nc_sec <= 0.5 * n:
            n_eff_sec = n - n_nc_sec
        else:
            n_eff_sec = int(0.5 * n)
        return 100 * (x['weight'].sum() / n_eff_sec)

    sec_scores = df.groupby('section').apply(section_score)
    sec_scores.plot(kind='barh', color='#3498db', edgecolor='black')
    plt.title('Figure 3: C_Score by Report Section', fontsize=12, fontweight='bold')
    plt.xlabel('C_Score')
    plt.axvline(60, color='green', linestyle='--', label='High Credibility')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, '03_section_comparison.png'), dpi=300)
    print("  [+] Saved 03_section_comparison.png")

    # Fig 05: Comparative Scores
    plt.figure(figsize=(8, 6))
    comp_data = {
        'Morgan Stanley\n(Actual)': final_c_score,
        'Hypothetical\nHigh Credibility': 95.0,
        'Hypothetical\nLow Credibility': 14.0
    }
    bars = plt.bar(comp_data.keys(), comp_data.values(),
                   color=['#3498db', '#2ecc71', '#e74c3c'],
                   edgecolor='black')
    plt.title('Figure 5: C_Score vs Benchmarks', fontsize=12, fontweight='bold')
    plt.ylabel('Score')
    plt.ylim(0, 110)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 2,
                 f'{bar.get_height():.1f}',
                 ha='center',
                 fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, '05_comparative_scores.png'), dpi=300)
    print("  [+] Saved 05_comparative_scores.png")

    # --- 3. SAVE RESULTS JSON ---
    results = {
    'weighted_sum': float(total_weighted_sum),
    'n_total': int(n_total),
    'n_eff': int(n_eff),
    'avg_fraction': float(avg_fraction),
    'penalties_applied': {k: int(v) for k, v in tactic_counts.items()},
    'penalty_sum': float(penalty_sum),
    'final_c_score': float(final_c_score),
    'section_scores': {k: float(v) for k, v in sec_scores.to_dict().items()}
}


    out_path = os.path.join(DOCS_DIR, 'validation_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\n[+] Analysis saved to docs/validation_results.json")


if __name__ == "__main__":
    main()
