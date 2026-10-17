# Evidence Before Assumption

> **Observe. Measure. Then conclude.**

Replace assumptions with observations. When uncertainty matters, instrument the system and measure it. Treat explanations as hypotheses until supported by reproducible evidence.

## Principle

**Do not assume what can be measured.**

- When uncertain, instrument and observe.
- Treat unexpected behavior as an evidence gap, not an invitation to speculate.
- Add diagnostics before attempting speculative fixes.
- State invariants explicitly and verify them at runtime where practical.
- Distinguish observed facts, verified facts, hypotheses, and unknowns.
- Prefer reproducible measurements over anecdotal observations.
- A fix is not understood until its effect can be observed and verified.

## Development Rule

**No unexplained behavior. No unmarked assumptions.**

If behavior is uncertain, measure it.

If behavior cannot be measured, instrument it.

If an assumption cannot yet be verified, label it explicitly as a hypothesis or unknown.

If a defect cannot be explained from available evidence, improve observability before changing behavior.

## Reasoning Loop

    Observation
        ↓
    Measurement
        ↓
    Hypothesis
        ↓
    Experiment / Reproduction
        ↓
    Verification Against Invariants
        ↓
    Conclusion
        ↓
    Change
        ↓
    Measurement of Resulting Behavior

Avoid:

    Symptom → Plausible Explanation → Code Change

Prefer:

    Symptom → Observation → Measurement → Hypothesis → Verification → Change → Measurement

The objective is not to eliminate hypotheses. Hypotheses are necessary for investigation.

The objective is to prevent **unverified hypotheses from becoming engineering facts**.