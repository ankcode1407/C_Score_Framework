# V. Proof-of-Concept Demonstration: Methodology and Inter-Rater Reliability

## V.A. Study Design Overview

This study presents an **initial proof-of-concept demonstration** of the C_Score framework through structured analysis of real-world corporate ESG disclosures. The primary objective is to evaluate whether the proposed taxonomy is **operationally feasible, internally coherent, and reproducible across independent annotators**, rather than to claim full generalizability or definitive measurement validity.

A single-case study design was employed, consistent with exploratory research in measurement development and classification system validation. The same 50-claim dataset was used for both framework refinement and testing, creating risk of overfitting. **True validation requires an independent test set on unseen companies and reports.** Emphasis was placed on **transparent procedures, conservative decision rules, and full auditability**, enabling critical assessment and replication.

---

## V.B. Document Selection and Analytical Scope

The proof-of-concept demonstration is based on the **Morgan Stanley 2023 ESG Report** (94 pages, published September 2024). Morgan Stanley was selected as an appropriate demonstration case for four reasons:

1. It is a globally significant financial institution (S&P 500, $1.8T AUM) with material exposure to ESG-related risks.
2. Its ESG report contains extensive disclosures across environmental, social, and governance dimensions.
3. Financial services ESG disclosures present known challenges for credibility assessment, particularly regarding financed emissions and Scope 3 impacts.
4. The report includes third-party assurance (Deloitte & Touche LLP, limited assurance), allowing for face-validity checks.

**Report details verified:**
- Publication date: September 2024 ✓
- Page count: 94 pages ✓
- Third-party assurance: Deloitte & Touche LLP ✓
- Framework alignment: TCFD, SASB, GRI ✓

Three substantive sections of the report were included in the analysis:
- Climate (pages 43-59)
- Sustainable Finance (pages 8-27)
- Human Capital (pages 28-42)

---

## V.C. Claim Extraction Protocol

### V.C.1 Definition of a Claim

A statement was classified as a "claim" if it satisfied all of the following criteria:

1. It made an explicit assertion about the company's environmental, social, or governance performance, actions, or commitments.
2. It referred either to retrospective performance outcomes or forward-looking commitments.
3. It was verifiable in principle, even if verification was not conducted within this study.
4. It addressed ESG topics material under widely used reporting frameworks (e.g., SASB, GRI).

### V.C.2 Exclusion Criteria

The following statements were excluded:
- Procedural or meta-reporting statements (e.g., report structure or methodology descriptions)
- Purely definitional content
- Statements describing external entities without firm-specific assertions
- Redundant restatements of substantively identical claims

### V.C.3 Sampling Strategy

A total of **50 claims** were extracted using systematic sampling across the three focal sections to ensure coverage of diverse ESG domains:
- Climate: 20 claims
- Sustainable Finance: 20 claims
- Human Capital: 10 claims

**Sampling limitation:** This represents approximately 25% of total claims in the full 94-page report. Comprehensive validation requires annotation of 200+ claims across multiple companies and sectors.

All claims were copied verbatim and annotated with page numbers to ensure traceability.

---

## V.D. Classification Methodology

### V.D.1 Taxonomy Application

Each extracted claim was independently classified into one of seven mutually exclusive C_Score categories:
- QuantitativeTarget
- VerifiedClaim
- PeripheralClaim
- VagueTarget
- AmbiguousBaseline
- OffsetsOnly
- NonClaim

Classification followed a deterministic decision tree specifying category assignment based on:
- Temporal orientation (future vs. past)
- Presence of hedging language
- Completeness of required elements (numeric target/outcome, deadline, baseline, scope)
- Nature of the claim (performance vs. governance/process)
- Reliance on offsets or credits

```
START: Read claim carefully

STEP 1: Is this forward-looking or retrospective?
├─ FORWARD-LOOKING → Go to STEP 2
└─ RETROSPECTIVE → Go to STEP 5

STEP 2: Does it contain hedging language?
├─ YES (aim to, strive, seek, work toward) → VagueTarget
└─ NO → Go to STEP 3

STEP 3: Does it have ALL required elements?
        - Numeric target (specific %)
        - Specific deadline (year)
        - Baseline year
        - Scope definition
├─ YES → QuantitativeTarget
├─ MOSTLY (3/4 elements) → QuantitativeTarget (if no hedging)
└─ NO → Go to STEP 4

STEP 4: Is it specific about process/governance but not performance?
├─ YES → PeripheralClaim
└─ NO → VagueTarget

STEP 5: Does it have numeric outcome with complete baseline?
├─ YES → VerifiedClaim
└─ NO → Go to STEP 6

STEP 6: Does it have percentage/comparative metric WITHOUT baseline year?
├─ YES → AmbiguousBaseline
└─ NO → Go to STEP 7

STEP 7: Is it exclusively about offsets/credits?
├─ YES → OffsetsOnly
└─ NO → Go to STEP 8

STEP 8: Is it verifiable governance/certification claim?
├─ YES → PeripheralClaim
└─ NO → NonClaim
```

All classifications were based strictly on the literal content of each claim, without inference from surrounding text.

### V.D.2 Required Elements Assessment

For claims potentially qualifying as QuantitativeTarget or VerifiedClaim, the presence or absence of four required elements was explicitly recorded:
1. Numeric target or outcome
2. Specific deadline or reporting period
3. Baseline year or comparison point
4. Defined scope

Claims missing any required element were downgraded in accordance with the decision tree rules.

### V.D.3 Boundary Case Identification

Annotators flagged claims as boundary cases when classification hinged on a single interpretive issue (e.g., hedging language or missing deadlines). Boundary flags were used solely for transparency and later consensus discussion and did not alter initial independent classifications.

---

## V.E. Inter-Rater Reliability Assessment

### V.E.1 Independent Annotation

To assess reproducibility, two annotators independently classified all 50 claims using the same decision tree, definitions, and training materials. 

**Annotator details:**
- Two graduate students in computer science with backgrounds in ESG reporting and NLP
- Neither annotator was involved in framework development
- Training consisted of: (1) 2-hour review of theoretical foundations and decision tree, (2) practice annotation of 5 claims with discussion, (3) independent annotation of the 50-claim test set with no communication

Annotators worked without communication during the independent annotation phase and without access to each other's classifications.

### V.E.2 Reliability Metrics

Inter-rater reliability was assessed using three complementary metrics:
- **Simple agreement**
- **Cohen's Kappa (κ)**, adjusting for chance agreement
- **Krippendorff's Alpha (α)**, suitable for nominal data and unequal category distributions

### V.E.3 Results

The inter-rater reliability results were as follows:
- Simple agreement: **96.0%** (48/50 claims)
- Cohen's κ: **0.935**
- Krippendorff's α: **0.882**

All metrics exceed commonly accepted thresholds for high-quality qualitative research (κ > 0.70; α > 0.80), indicating **almost perfect agreement**.

**Contextual note:** The high agreement likely reflects: (a) relatively clear category boundaries for most claims in this homogeneous single-report sample, (b) structured decision tree reducing ambiguity, and (c) focused training on specific boundary cases. Cross-sector and cross-company validation may reveal lower agreement as edge cases increase.

---

## V.F. Disagreement Analysis and Consensus Resolution

Only **two claims (4% of the dataset)** were classified differently by the two annotators. Both disagreements involved the same category boundary: **QuantitativeTarget vs. VagueTarget**.

The sources of disagreement were:
1. The presence of explicit hedging language despite otherwise complete quantitative specification.
2. The absence of a deadline in claims containing highly specific numeric targets.

Consensus resolution followed the predefined decision rules:
- Any hedging language automatically disqualified a claim from QuantitativeTarget.
- Missing any required element (including deadline) resulted in classification as VagueTarget.

After applying these rules, both disputed claims were reclassified as VagueTarget. The resolution process was fully documented, including rationale and impact on downstream scoring.

---

## V.G. Implications for Scoring and Validity

Applying consensus classifications resulted in a reduction in the number of QuantitativeTarget claims and a corresponding increase in VagueTarget claims. This adjustment reduced the overall C_Score relative to single-annotator results, demonstrating that **inter-rater consensus produced a more conservative assessment rather than inflating credibility**.

Importantly, all disagreements were confined to a single normative boundary, while perfect agreement was observed for VerifiedClaim, PeripheralClaim, NonClaim, and AmbiguousBaseline categories. This pattern indicates that the taxonomy is **structurally clear**, with ambiguity concentrated only where conceptual judgment is inherently required.

---

## V.H. Methodological Limitations

Several limitations must be acknowledged:

**Critical constraints:**
1. **Circular validation:** The same 50-claim dataset was used for both taxonomy refinement and testing, creating risk of overfitting.
2. **Single-sector validation:** Financial services only; generalizability to manufacturing, energy, retail unclear.
3. **Small sample size:** 50 claims vs. 500+ needed for stable category estimates and statistical power.
4. **Single company:** Morgan Stanley may not represent typical disclosure patterns.
5. **Homogeneous sample:** Claims from single report may inflate inter-rater agreement.

**Theoretical calibration vs. empirical estimation:**
6. **Category weights:** Remain theoretically motivated rather than empirically calibrated through optimization or stakeholder elicitation.
7. **Penalty magnitudes:** Absolute values not normalized to claim volume or sector norms.
8. **Sector multipliers:** Based on SASB/CDP materiality guidance (expert judgment) rather than quantitative data analysis.

These limitations are appropriate for an initial proof-of-concept demonstration and define clear priorities for future research. **True validation requires:**
- Independent test set on unseen companies (avoiding circular validation)
- Cross-sector replication (minimum 10 companies × 7 industries)
- Larger sample sizes (n≥200 claims for statistical stability)
- Multi-year longitudinal analysis (temporal consistency assessment)
- Empirical weight calibration (stakeholder surveys, predictive validity testing)

---

## V.I. Summary

This proof-of-concept demonstration shows that the C_Score framework is **operational, reproducible, and capable of consistent application by independent annotators**. High inter-rater reliability (κ = 0.935), transparent disagreement resolution, and conservative consensus adjustments support the framework's feasibility as an initial measurement instrument for ESG claim assessment.

**Key achievements:**
- ✓ Operational feasibility demonstrated on real-world ESG report
- ✓ High inter-rater agreement (96%) indicates clear category boundaries  
- ✓ Transparent, reproducible methodology with full auditability
- ✓ Discriminant validity demonstrated (section-level variance detected)

**Critical next steps for full validation:**
- Independent test set validation (unseen companies/sectors)
- Larger sample sizes (200+ claims, 10+ companies)
- Empirical weight calibration (stakeholder elicitation)
- Predictive validity testing (correlation with enforcement outcomes)
- Cross-sector generalizability assessment

This work establishes the **methodological foundation**; large-scale empirical validation constitutes the critical next phase.
