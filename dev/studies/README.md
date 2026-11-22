# Studies

Evidence-backed examinations of the repository, running system, architecture, tooling,
or development approach at a specific point in time.

A study gathers evidence, records findings, and may produce decisions, recommendations,
backlog items, or follow-up work. Studies do not require a fixed structure, but every
conclusion must be traceable to documented evidence.

Each study has its own folder under `dev/studies/`. The folder `README.md` is the
authoritative record.
`open-questions.md` file captures the questions in simple words that need to be answered.
Questions are listed with provided context, recommendations and why they are important.

```text
studies/
├── README.md
├── <study-topic>/
│   ├── README.md
│   ├── open-questions.md
│   ├── evidence/
│   └── ...
└── ...
```