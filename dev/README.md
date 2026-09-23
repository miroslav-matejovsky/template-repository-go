# Dev

Working records that drive the evolution of this repository. They are not user or API
documentation. Architecture overview lives in the root `README.md`; package documentation
lives in each Go package's `doc.go`.

Each folder has its own `README.md` that defines its file format and holds its index.

| Folder | Purpose |
| --- | --- |
| [`plans/`](plans/README.md) | Active implementation plans. Executable specifications split into numbered steps. |
| [`backlog/`](backlog/README.md) | Open implementation and tuning work not yet planned, one item per file. |
| [`bugs/`](bugs/README.md) | Confirmed defects awaiting a fix, one bug per file. |
| [`assessments/`](assessments/README.md) | Evidence-backed reviews of the repository at a specific revision. |
| [`evaluations/`](evaluations/README.md) | Technical evaluations and decisions that support code evolution. |

## Flow

- Assessments and evaluations produce findings and decisions.
- Findings become bugs or backlog items.
- Backlog items and bugs selected for work become plans.
- Finished work is removed. Git history is the record of completed work.
- Actionable items outside these records, such as live verification, go in the root `.todo`.
