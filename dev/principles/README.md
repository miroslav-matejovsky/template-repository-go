# Principles

Principles capture the architectural and domain truths that define a system.
Unlike technologies, frameworks, implementation details or coding conventions, principles describe how a system understands its problem space and how important decisions should be made.
A good principle remains valid even if the implementation changes completely.

Principles always apply. Consider them before every decision and evaluate studies, plans,
and changes against them. When a decision conflicts with a principle, state the conflict
and the reason in the work that makes it.

One principle per file. Each file names the principle, states the rules it implies, and
gives a development rule that makes it checkable.

| Principle | Description |
|-----------|-------------|
| [Configuration Is Documentation](configuration.md) | Operationally significant behavior is explicitly configurable, documented, visible, and owned. |
| [Evidence Before Assumption](evidence.md) | Observe and measure before concluding, so unverified hypotheses never become engineering facts. |
