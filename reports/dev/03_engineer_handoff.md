# Engineer handoff

## Candidate

- Candidate application commit: `86f30dc353dda2aaf5ce8f8a292980c26983f94c`
- Branch: `improvement/offline-foundation-v1`

## Changed files

- `ProjectMayhem/main.py`
- `tests/test_engineering.py`
- `tests/__init__.py`
- `.github/workflows/offline-tests.yml`

## Behaviour changes

`main.py` removed module-level broker login and embedded credential assignments, added lazy MT5 import and explicit `connect_broker()`/`shutdown_broker()` lifecycle functions, and reads broker configuration from environment variables at explicit startup. The M15 incremental writer selects the final row as a one-row DataFrame, avoiding the previous `Series.iterrows()` defect. Empty input was intended to produce no output. Existing CSV columns and serialization were intended to remain unchanged.

Tests and discovery support were added, and workflow discovery was updated to `python -m unittest discover -s tests -p 'test_*.py' -v` with repository-root `PYTHONPATH`.

## Engineer execution evidence

The engineer reported Python 3.11.6 and attempted the required unittest command, but the sandbox working-directory/file state was unavailable to the shell runner. It returned: `ImportError: Start directory is not importable: 'tests'`. No test count or executed test names were produced by that attempt. The engineer reported that the repository commit was created successfully.

The candidate was therefore implemented but awaiting execution at that handoff. Previously exposed credentials remain in repository history and require separate rotation.
