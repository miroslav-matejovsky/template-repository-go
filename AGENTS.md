# AGENTS.md

- Never commit changes - NEVER!
- Talk like a Caveman - Short sentences, simple words, no fluff, avoid "the", "a", "an", "this", "that", etc.
- Be concise in output but thorough in reasoning.
- No sycophantic openers or closing fluff.
- Think before acting. Read existing files before writing code.
- Prefer editing over rewriting whole files.
- Do not re-read files you have already read unless the file may have changed.
- Keep solutions simple and direct.
- When unclear, describe the problem and ask for clarification, or write to the local text file and stop.
- Before completing a task, run 'task all' to ensure all tests pass and code is formatted. 'task all' must pass before work is considered complete!
- This is just experimentation phase, no need to worry about breaking things or backwards compatibility. Focus on making progress and clean, simple code without worrying about stored data - we can always delete and start fresh if needed.

## Documentation

- Use root `README.md` as a reference for project overview and high-level architecture.
- Always read `doc.go` files in each package to understand the domain concepts and design decisions before modifying or adding code.
- If a `doc.go` file is missing, create one with comprehensive documentation to explain the domain concepts and design decisions. This is crucial for maintainability and onboarding new developers.
- Always update `doc.go` files in each package to explain any changes to the domain concepts and design decisions. This is crucial for maintainability and onboarding new developers.
- Document fields in significant data structures to explain their purpose and constraints.
- If folder is not a go package, use a `README.md` to understand the folder's purpose and contents.
- If a `README.md` is missing for a non-package folder, create one with comprehensive documentation to explain the folder's purpose and contents. This is crucial for maintainability and onboarding new developers.
- Always update `README.md` files for non-package folders to explain any changes to the folder structure or contents. This is crucial for maintainability and onboarding new developers.
- Documentation and comments in code must be self-contained, no references to external documents or files. This is crucial for maintainability.

## Environment and Tooling

- Use `gopls` to find definitions and references in go code.
- Use `go doc` to understand Go code and libraries.

## Coding Style

- Always prefer boring, pragmatic, and idiomatic Go code over clever or complex solutions.
- Write clear and concise Go docs for all exported functions, types, attributes, and packages.
- Write docs for internal packages and unexported functions as well, but use a less formal style.
- Always prefer composition over inheritance.
- Use KISS principle - simple, direct solutions are preferred over complex ones.
- Use YAGNI principle - do not implement features until they are actually needed.
- Code duplication is acceptable - do not abstract code until you have at least 3 instances of it.
- Avoid premature optimization. Write clear code first, optimize later if needed.
- Never swallow errors. Handle them explicitly or bubble them up with meaningful context and message.
- Fail fast: validate configurations and constraints as early as possible (e.g. in constructors rather than during execution).
- Use `require` assertions from the `testify` library for unit tests.

## Output

- Return code first. Explanation after, only if non-obvious.
- No boilerplate unless explicitly requested.
- No em dashes, smart quotes, or decorative Unicode symbols.
- Plain hyphens and straight quotes only.
- Natural language characters (accented letters, CJK, etc.) are fine when the content requires them.
- Code output must be copy-paste safe.
- Pipeline calls compound. Every token saved per call multiplies across runs.
- No explanatory text in agent output unless a human will read it.
- Return the minimum viable output that satisfies the task spec.
- When implementation is not completed or stubs are used, document missing pieces in the `.todo` file with clear instructions in the root of the project.
