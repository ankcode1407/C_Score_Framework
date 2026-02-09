# V. Empirical Validation Methodology and Inter-Rater Reliability

## V.A. Study Design Overview

This study presents an initial empirical validation of the C_Score framework through structured analysis of real-world corporate ESG disclosures. The primary objective is to evaluate whether the proposed taxonomy is **operationally feasible, internally coherent, and reproducible across independent annotators**, rather than to claim full generalizability or definitive measurement validity.

A single-case study design was employed, consistent with exploratory research in measurement development and classification system validation. Emphasis was placed on **transparent procedures, conservative decision rules, and full auditability**, enabling critical assessment and replication.

---

## V.B. Document Selection and Analytical Scope

The empirical validation is based on the **Morgan Stanley 2023 ESG Report** (94 pages). Morgan Stanley was selected as an appropriate validation case for four reasons:

1. It is a globally significant financial institution with material exposure to ESG-related risks.
2. Its ESG report contains extensive disclosures across environmental, social, and governance dimensions.
3. Financial services ESG disclosures present known challenges for credibility assessment, particularly regarding financed emissions and Scope 3 impacts.
4. The report claims third-party assurance, allowing for face-validity checks.

Three substantive sections of the report were included in the analysis:
- Climate
- Sustainable Finance
- Human Capital

---

## V.C. Claim Extraction Protocol

### V.C.1 Definition of a Claim

A statement was classified as a “claim” if it satisfied all of the following criteria:

1. It made an explicit assertion about the company’s environmental, social, or governance performance, actions, or commitments.
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

To assess reproducibility, two annotators independently classified all 50 claims using the same decision tree, definitions, and training materials. Annotators worked without communication and without access to each other’s classifications.

### V.E.2 Reliability Metrics

Inter-rater reliability was assessed using three complementary metrics:
- **Simple agreement**
- **Cohen’s Kappa (κ)**, adjusting for chance agreement
- **Krippendorff’s Alpha (α)**, suitable for nominal data and unequal category distributions

### V.E.3 Results

The inter-rater reliability results were as follows:
- Simple agreement: **96.0%**
- Cohen’s κ: **0.935**
- Krippendorff’s α: **0.882**

All metrics exceed commonly accepted thresholds for high-quality qualitative research (κ > 0.70; α > 0.80), indicating **almost perfect agreement**.

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

Applying consensus classifications resulted in a reduction in the number of QuantitativeTarget claims and a corresponding increase in VagueTarget claims. This adjustment reduced the overall C_Score relative to the single-annotator result, demonstrating that **inter-rater consensus produced a more conservative assessment rather than inflating credibility**.

Importantly, all disagreements were confined to a single normative boundary, while perfect agreement was observed for VerifiedClaim, PeripheralClaim, NonClaim, and AmbiguousBaseline categories. This pattern indicates that the taxonomy is **structurally clear**, with ambiguity concentrated only where conceptual judgment is inherently required.

---

## V.H. Methodological Limitations

Several limitations should be acknowledged:
- The study is based on a single company and reporting year.
- Only two annotators were used.
- Category weights remain theoretically motivated rather than empirically calibrated.
- Penalty magnitudes are absolute rather than normalized to claim volume.

These limitations are appropriate for an initial validation and define clear priorities for future research.

---

## V.I. Summary

This empirical validation demonstrates that the C_Score framework is **operational, reproducible, and capable of consistent application by independent annotators**. High inter-rater reliability, transparent disagreement resolution, and conservative consensus adjustments support the framework’s credibility as an initial measurement instrument for ESG claim assessment.
