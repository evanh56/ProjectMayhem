# Consolidated implementation report — offline foundation v1

**Date:** 2026-10-22  
**Repository:** `evanh56/ProjectMayhem`  
**Development branch:** `improvement/offline-foundation-v1`  
**Base:** `main`

## Status

**Tests failed.** The candidate has a completed independent QA sandbox result with 9 discovered tests, 8 passing and 1 error. No completed successful GitHub Actions run matching the candidate SHA was supplied. Therefore this increment is not fully validated.

## Concrete problem and changed behaviour

The baseline application imported MT5 and logged in from module scope, contained credential assignments in current source, and had an invalid M15 incremental writer path: `data.iloc[-1]` returned a pandas `Series`, after which `.iterrows()` was attempted. The scoped implementation removed import-time broker activity, moved broker startup to explicit lifecycle functions with environment-based configuration, removed current-source credential values, and changed incremental selection to a one-row DataFrame. It added offline regression tests, test-package support, and unittest discovery in CI.

The candidate also intended empty input to produce no output, but QA showed that empty incremental input is indexed before the guard and raises an `IndexError`. This is the remaining scoped defect.

## Baseline and revisions

- Selected baseline `main`: `8feb36db91d7144b4a190a302634ddd30c449c0b`
- Audit branch audit commit: `8c33a68fb5c46c510170050c5262c8ef74dfa020`
- Development branch pre-candidate: `b23f47b4b0e294b29bc69c5c2a8ae643a712d648`
- Candidate application commit: `86f30dc353dda2aaf5ce8f8a292980c26983f94c`
- Candidate tested revision: `86f30dc353dda2aaf5ce8f8a292980c26983f94c` in the independent QA sandbox copy

The report-only commit created for these handoffs is separate from the application candidate commit.

## Files changed by the application candidate

- `ProjectMayhem/main.py`
- `tests/test_engineering.py`
- `tests/__init__.py`
- `.github/workflows/offline-tests.yml`

The report-only commit changes only `reports/dev/` and must not trigger the offline workflow because the workflow path filter excludes reports.

## Handoff summaries

### Baseline

`main` was selected because it contains the latest application tree and newer workflow; the audit branch adds reports rather than newer application implementation.

### Researcher

Authorised only offline-safe imports, explicit startup, removal of current credential values, M15 append repair, regression tests, and discovery. Strategy definitions and duplicate/completed-candle semantics remain unchanged and unresolved.

### Engineer

Implemented explicit broker lifecycle, environment configuration, one-row DataFrame incremental writing, regression tests, `tests/__init__.py`, and discovery configuration. Engineer sandbox execution was blocked by a filesystem mismatch and produced no test evidence.

### QA

QA sandbox discovered 9 tests: 8 passed and 1 failed. Import isolation, credential source check, normal append, and all starter tests passed. Empty incremental input failed before the guard. Workflow configuration passed static review.

### Risk

The candidate is not approved for paper or live trading. Execution, sizing, stops, exposure limits, stale-data handling, reconciliation, failure recovery, and historical secret remediation remain material risks.

## Execution evidence

### (a) Engineer sandbox runs

The engineer reported Python 3.11.6 and attempted:

```text
python -m unittest discover -s tests -p 'test_*.py' -v
```

It failed before test execution because the sandbox file and shell roots differed:

```text
ImportError: Start directory is not importable: 'tests'
```

No test count or test names were produced by that attempt. This was a sandbox attempt, not GitHub Actions.

### (b) Independent QA sandbox runs

QA ran the same discovery command on a copy of the committed files in a Python 3.13 environment without MT5 or broker access.

```text
Ran 9 tests in 0.073s
FAILED (errors=1)
RETURN 1
```

Eight tests passed and one failed: `test_empty_incremental_input_writes_nothing`, with `IndexError: positional indexers are out-of-bounds` at `data.iloc[[-1]]`. The five starter tests passed, as did normal append, import isolation, source credential checking, syntax, and discovery.

Sandbox results are not GitHub Actions results.

### (c) GitHub Actions runs on the candidate SHA

A matching run was reported:

- Run ID `39696807306`
- Head SHA `86f30dc353dda2aaf5ce8f8a292980c26983f94c`
- Status `in_progress`
- Conclusion unavailable/null

No completed candidate result, artifact, or log was supplied. A successful run for `b23f47b4b0e294b29bc69c5c2a8ae643a712d648` was historical and does not validate the candidate. No workflow was dispatched or rerun.

### (d) Statically inspected checks

- Workflow retains `workflow_dispatch` and push only for `improvement/offline-foundation-v1` with the four requested path filters.
- Workflow has read-only contents permission, disabled checkout credentials, five-minute timeout, Python 3.11, repository-root `PYTHONPATH`, and the requested discovery command.
- Candidate branch verification reported head `86f30dc353dda2aaf5ce8f8a292980c26983f94c`.
- QA static review found no current credential values in reviewed sources; values are not reproduced here.
- No strategy formulas or risk definitions were intentionally changed according to the handoffs.

## Remaining limitations and blockers

1. Fix empty incremental input before acceptance.
2. Obtain a completed successful GitHub Actions run whose head SHA equals `86f30dc353dda2aaf5ce8f8a292980c26983f94c`; only then may the increment be called fully validated.
3. Previously exposed MT5 credentials remain in repository history and must be rotated/revoked; current values are intentionally omitted and any credential values encountered are treated as `[REDACTED]`.
4. No trading approval: order execution remains incomplete and risk, stops, broker constraints, exposure controls, stale-data handling, and reconciliation are not verified.
5. Duplicate timestamp and completed-candle policies remain unresolved.
6. Sandbox evidence is not CI evidence.

## Backlog carried forward

- Correct empty incremental writer guard and rerun all tests.
- Produce completed matching CI evidence and retain logs/artifacts.
- Rotate/revoke historically exposed credentials and document remediation without reproducing secrets.
- Later define completed-candle and duplicate policies.
- Later address account-currency sizing, costs, conversion, volume constraints, stops, execution idempotency, rejection/partial-fill handling, stale data, restart recovery, broker reconciliation, aggregate/shared-JPY exposure, daily loss, and drawdown controls.
- Do not expand this increment into strategy redesign, broker connection, or production execution.

## Usage and cost

Usage and cost are **unverified**; no usage or cost evidence was supplied.

## Defined next increment

Repair `write_15m()` so empty input returns before selecting `data.iloc[[-1]]`. Run `python -m unittest discover -s tests -p 'test_*.py' -v` against the resulting candidate, then obtain a completed GitHub Actions run with a successful conclusion whose head SHA exactly equals that candidate commit. Keep the next change scoped to the empty-input defect and its evidence.

## Pull-request intent

A pull request is requested from `improvement/offline-foundation-v1` into `main` with title `Offline foundation v1: safe imports, credential removal, M15 append repair`. The branch is not to be merged by this delivery.
