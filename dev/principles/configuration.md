# Configuration Is Documentation

Declare what matters. Document what can vary. Expose what operators need.

Configuration captures operational choices that are intentionally adjustable across environments, deployments, or operating conditions.

- Make operationally significant values configurable when there is a legitimate reason to change them without modifying code.
- Sensible, documented defaults are acceptable. Require explicit values where safety, security, or correctness demands them.
- Validate required configuration early and report invalid or missing values clearly.
- Document purpose, units, expected values, and operational impact where relevant.
- Keep stable implementation details and internal constants in code when configurability provides no meaningful operational benefit.
- Make important effective configuration observable for troubleshooting and operational understanding.

Guiding rule: Operators should be able to understand and control important operational behavior without reading source code, but not every value that influences behavior needs to become configuration.