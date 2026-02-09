"""
FILE: reliability_check.py
AUTHOR: Shaurya Mishra (Amity University)
PURPOSE: Inter-Rater Reliability Analysis (Annotator 1 vs Annotator 2).
         Generates Figures 12-13 and JSON statistics.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# --- 1. DYNAMIC PATH SETUP ---
# This determines the root folder automatically based on where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIS_DIR = os.path.join(BASE_DIR, 'visualizations')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Create output directories if they don't exist
for d in [VIS_DIR, DOCS_DIR]:
    os.makedirs(d, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-muted')

print("="*80)
print("INTER-RATER RELIABILITY ANALYSIS")
print("C_Score Framework - Morgan Stanley Dataset")
print("="*80)

# --- 2. LOAD DATA ---
try:
    original = pd.read_csv(os.path.join(DATA_DIR, 'morgan_stanley_claims_dataset.csv'))
    annotator2 = pd.read_csv(os.path.join(DATA_DIR, 'annotator2_classifications.csv'))
except FileNotFoundError as e:
    print(f"[!] CRITICAL ERROR: Input files missing in {DATA_DIR}")
    print(f"    Ensure 'morgan_stanley_claims_dataset.csv' and 'annotator2_classifications.csv' are in the /data folder.")
    exit()

# Merge datasets
comparison = original[['claim_id', 'verbatim_text', 'category', 'boundary_case']].copy()
comparison.columns = ['claim_id', 'verbatim_text', 'annotator1_category', 'annotator1_boundary']
comparison = comparison.merge(annotator2[['claim_id', 'annotator2_category', 'annotator2_boundary_case']], 
                              on='claim_id')
comparison.columns = ['claim_id', 'verbatim_text', 'annotator1', 'ann1_boundary', 'annotator2', 'ann2_boundary']

# Calculate agreement
comparison['agree'] = comparison['annotator1'] == comparison['annotator2']
total_claims = len(comparison)
agreements = comparison['agree'].sum()
disagreements = total_claims - agreements
simple_agreement = agreements / total_claims

print(f"\n{'─'*80}")
print("1. SIMPLE AGREEMENT")
print(f"{'─'*80}")
print(f"Total claims: {total_claims}")
print(f"Agreements: {agreements} ({simple_agreement*100:.1f}%)")
print(f"Disagreements: {disagreements} ({(1-simple_agreement)*100:.1f}%)")

# Cohen's Kappa
kappa = cohen_kappa_score(comparison['annotator1'], comparison['annotator2'])

print(f"\n{'─'*80}")
print("2. COHEN'S KAPPA (Agreement Adjusted for Chance)")
print(f"{'─'*80}")
print(f"κ = {kappa:.3f}")

# Interpretation
if kappa < 0: interpretation = "Poor (worse than chance)"
elif kappa < 0.20: interpretation = "Slight agreement"
elif kappa < 0.40: interpretation = "Fair agreement"
elif kappa < 0.60: interpretation = "Moderate agreement"
elif kappa < 0.80: interpretation = "Substantial agreement"
else: interpretation = "Almost perfect agreement"

print(f"Interpretation: {interpretation}")
print(f"\nBenchmark for publication:")
print(f"  κ > 0.70: Acceptable for research (SUBSTANTIAL)")
print(f"  κ > 0.80: Excellent (ALMOST PERFECT)")
print(f"  Current: κ = {kappa:.3f} → {interpretation.upper()}")

#  DISAGREEMENT & BOUNDARY ANALYSIS ---
print(f"\n{'─'*80}")
print("DISAGREEMENT & BOUNDARY ANALYSIS")
print(f"{'─'*80}")

disagreements_df = comparison[~comparison['agree']].copy()
boundary_either = comparison[(comparison['ann1_boundary']) | (comparison['ann2_boundary'])]
boundary_both = comparison[(comparison['ann1_boundary']) & (comparison['ann2_boundary'])]
boundary_agreement = boundary_either['agree'].mean() if len(boundary_either) > 0 else 0.0

if len(disagreements_df) > 0:
    print(f"\nDisagreements by category pair:")
    for idx, row in disagreements_df.iterrows():
        print(f"\n  Claim {row['claim_id']}:")
        print(f"    Annotator 1: {row['annotator1']}")
        print(f"    Annotator 2: {row['annotator2']}")
        print(f"    Text: {row['verbatim_text'][:100]}...")
        if row['ann1_boundary'] or row['ann2_boundary']:
            print(f"    ⚠️ BOUNDARY CASE (flagged by at least one annotator)")
else:
    print("No disagreements!")

# Disagreement analysis
print(f"\n{'─'*80}")
print("3. DISAGREEMENT ANALYSIS")
print(f"{'─'*80}")

disagreements_df = comparison[~comparison['agree']].copy()
if len(disagreements_df) > 0:
    print(f"\nDisagreements by category pair:")
    for idx, row in disagreements_df.iterrows():
        print(f"\n  Claim {row['claim_id']}:")
        print(f"    Annotator 1: {row['annotator1']}")
        print(f"    Annotator 2: {row['annotator2']}")
        print(f"    Text: {row['verbatim_text'][:100]}...")
        if row['ann1_boundary'] or row['ann2_boundary']:
            print(f"    ⚠️ BOUNDARY CASE (flagged by at least one annotator)")
else:
    print("No disagreements!")

# Category-specific agreement
print(f"\n{'─'*80}")
print("4. PER-CATEGORY AGREEMENT")
print(f"{'─'*80}")

categories = sorted(set(comparison['annotator1'].unique()) | set(comparison['annotator2'].unique()))
print(f"\nCategories in dataset: {', '.join(categories)}")

category_agreement = {}
for cat in categories:
    ann1_cat = comparison[comparison['annotator1'] == cat]
    precision = (ann1_cat['agree'].sum() / len(ann1_cat)) * 100 if len(ann1_cat) > 0 else np.nan
    
    ann2_cat = comparison[comparison['annotator2'] == cat]
    recall = (ann2_cat['agree'].sum() / len(ann2_cat)) * 100 if len(ann2_cat) > 0 else np.nan
    
    category_agreement[cat] = {
        'annotator1_count': len(ann1_cat),
        'annotator2_count': len(ann2_cat),
        'precision': precision,
        'recall': recall
    }

agreement_df = pd.DataFrame(category_agreement).T
print("\n", agreement_df.to_string())

# Confusion matrix
print(f"\n{'─'*80}")
print("5. CONFUSION MATRIX")
print(f"{'─'*80}")

cm = confusion_matrix(comparison['annotator1'], comparison['annotator2'], labels=categories)
cm_df = pd.DataFrame(cm, index=categories, columns=categories)
print("\nRows = Annotator 1, Columns = Annotator 2")
print("Diagonal values = agreements\n")
print(cm_df.to_string())

# Krippendorff's Alpha Function (User Provided)
def krippendorff_alpha_nominal(data1, data2):
    n = len(data1)
    categories_all = sorted(set(data1) | set(data2))
    n_cat = len(categories_all)
    cat_to_idx = {cat: i for i, cat in enumerate(categories_all)}
    
    o = np.zeros((n_cat, n_cat))
    for v1, v2 in zip(data1, data2):
        i, j = cat_to_idx[v1], cat_to_idx[v2]
        o[i, j] += 1
        if i != j: o[j, i] += 1
    
    n_total = o.sum()
    n_c = o.sum(axis=1)
    D_o = 0
    for i in range(n_cat):
        for j in range(n_cat):
            if i != j: D_o += o[i, j]
    
    D_e = 0
    for i in range(n_cat):
        for j in range(n_cat):
            if i != j: D_e += n_c[i] * n_c[j]
    
    D_o = D_o / n_total
    D_e = D_e / (n_total * (n_total - 1))
    
    if D_e == 0: alpha = 1.0
    else: alpha = 1 - (D_o / D_e)
    
    return alpha

alpha = krippendorff_alpha_nominal(comparison['annotator1'].values, comparison['annotator2'].values)

print(f"\n{'─'*80}")
print("8. KRIPPENDORFF'S ALPHA")
print(f"{'─'*80}")
print(f"α = {alpha:.3f}")

# --- VISUALIZATIONS ---
print(f"\n{'─'*80}")
print("GENERATING VISUALIZATIONS")
print(f"{'─'*80}")

# Visualization 1: Confusion Matrix Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'},
            linewidths=0.5, linecolor='gray', ax=ax)
ax.set_title('Inter-Rater Confusion Matrix\n(Diagonal = Agreement)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Annotator 2 Classification', fontsize=12, fontweight='bold')
ax.set_ylabel('Annotator 1 Classification', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

# Save to Visualization Folder
save_path_12 = os.path.join(VIS_DIR, '12_confusion_matrix.png')
plt.savefig(save_path_12, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {save_path_12}")

# Visualization 2: Agreement Metrics
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Simple agreement vs kappa
metrics = ['Simple\nAgreement', "Cohen's κ", "Krippendorff's α"]
values = [simple_agreement, kappa, alpha]
colors = ['#3498db', '#2ecc71', '#9b59b6']
bars = ax1.bar(metrics, values, color=colors, alpha=0.8)

ax1.set_ylabel('Agreement Score', fontsize=12, fontweight='bold')
ax1.set_title('Inter-Rater Reliability Metrics', fontsize=14, fontweight='bold', pad=20)
ax1.set_ylim([0, 1])
ax1.axhline(y=0.70, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Acceptable (0.70)')
ax1.axhline(y=0.80, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Excellent (0.80)')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Per-category agreement
cats_with_data = agreement_df[agreement_df['annotator1_count'] > 0].index
precisions = agreement_df.loc[cats_with_data, 'precision'].values
x_pos = np.arange(len(cats_with_data))

bars2 = ax2.barh(x_pos, precisions, color='steelblue', alpha=0.8)
ax2.set_yticks(x_pos)
ax2.set_yticklabels(cats_with_data, fontsize=10)
ax2.set_xlabel('Agreement Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Agreement Rate by Category', fontsize=14, fontweight='bold', pad=20)
ax2.set_xlim([0, 110])
ax2.axvline(x=80, color='green', linestyle='--', linewidth=1, alpha=0.5, label='80% threshold')
ax2.legend()
ax2.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars2, precisions)):
    if not np.isnan(val):
        ax2.text(val + 2, i, f'{val:.1f}%', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
# Save to Visualization Folder
save_path_13 = os.path.join(VIS_DIR, '13_agreement_metrics.png')
plt.savefig(save_path_13, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {save_path_13}")

# Save detailed results to JSON
results = {
    'overall': {
        'total_claims': int(total_claims),
        'agreements': int(agreements),
        'disagreements': int(disagreements),
        'simple_agreement': float(simple_agreement),
        'cohens_kappa': float(kappa),
        'krippendorffs_alpha': float(alpha),
        'interpretation': interpretation
    },
    'disagreements': disagreements_df[['claim_id', 'annotator1', 'annotator2', 'verbatim_text']].to_dict('records'),
    'category_agreement': agreement_df.to_dict(),
    'boundary_cases': {
        'flagged_by_either': int(len(boundary_either)),
        'flagged_by_both': int(len(boundary_both)),
        'agreement_on_boundary': float(boundary_agreement) if len(boundary_either) > 0 else None
    }
}

# Save to Docs Folder (Correct location for reports)
json_path = os.path.join(DOCS_DIR, 'inter_rater_reliability.json')
with open(json_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'─'*80}")
print("ANALYSIS COMPLETE")
print(f"{'─'*80}")
print(f"📊 Final Kappa: {kappa:.3f}")
print(f"📁 Images saved to: {VIS_DIR}")
print(f"📁 JSON saved to:   {DOCS_DIR}")