# Baseline record

The source supplied a baseline record for `evanh56/ProjectMayhem`.

## Selected baseline

- `main`: `8feb36db91d7144b4a190a302634ddd30c449c0b`
- Audit branch commit discussed: `8c33a68fb5c46c510170050c5262c8ef74dfa020`
- Development branch before the candidate: `b23f47b4b0e294b29bc69c5c2a8ae643a712d648`
- Selected baseline: `main` at `8feb36db91d7144b4a190a302634ddd30c449c0b`

The audit branch was reported to contain audit documentation rather than newer application code. The current `main` workflow was reported as newer and includes the development-branch push trigger. No repository writes were performed during the supplied inspection.

## Scope mapping

Implementation, tests, requirements, workflow, and documentation are taken from `main`; audit reports are documentation only. The supplied comparison reported identical requested application Python files and `tests/test_offline.py` between `main` and the audit branch.

## Existing findings

The supplied record identified import-time MT5 login and embedded credentials in `ProjectMayhem/main.py`, an invalid incremental CSV append path, incomplete execution and risk controls, unresolved candle-completion and duplicate semantics, and historical workflow evidence that did not validate the current `main` head.
