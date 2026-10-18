# Project Mayhem — experiment log

Updated: 18 October 2026. Version: 0.1. Status: initial documentation baseline.

Paths in this document are relative to the project root unless a Markdown link is used.

## Recording rules

This log distinguishes documentation/static checks, offline tests, historical simulations, paper trades and live observations. Do not label one as another. No P&L, win rate, drawdown or profit factor is available from the checks performed here.

Every result must reference actual evidence. Record failed and inconclusive experiments. Do not manufacture favourable outcomes or treat selected winning screenshots as a complete sample.

## EXP-000 — uploaded baseline inspection

- **Date:** 18 October 2026, Europe/Dublin.
- **Type:** File inventory, source inspection, CSV inspection and syntax parsing.
- **Status:** Completed within this limited scope; no trading performance conclusion.
- **Purpose:** Ground the six agent documents in the supplied project.
- **Input:** The supplied `Project Mayhem Team.zip` and the current owner brief.
- **Source baseline:** Six Python files in `src/ProjectMayhem/`.
- **Code fingerprint:** `8094a99de0f77443eeb0b2031a934f6a9a820dffedfd211d66d4445d750da444`.
- **Fingerprint method:** SHA-256 over sorted Python filenames, each followed by a NUL byte and the original file bytes, concatenated.
- **Data:** Seven supplied CSV snapshots; individual hashes and row counts are in [data dictionary](data_dictionary.md).
- **Procedure:** Inventory project files excluding environment and metadata for review; read all six source modules and `Strategy.txt`; parse the six modules with Python `ast.parse`; inspect CSV headers, counts and first/last records; inspect `Phase2Map.png` and the first-page embedded preview of `Automatic Trading Software.pages`.
- **Verified results:** Six of six modules parsed successfully. Seven CSV files contain 333 total data rows across raw bars and derived outputs (1 + 192 + 120 + 2 + 1 + 1 + 16). No supplied test files or project-owned dependency manifest was found outside the bundled environment. Strategy and trade execution are incomplete. Code selects GBPJPY while filenames retain GBPUSD. USDJPY is not separately represented.
- **Source findings:** F01–F10 in [project overview](project_overview.md). These were inspected statically; exception paths and profitability were not executed.
- **Not performed:** Importing/running application modules, dependency installation, broker authentication, detector execution, backtesting, paper/live orders, account access, full Pages conversion or complete research review.
- **Outcome:** Suitable for an initial source/specification audit. Not sufficient to claim runtime readiness, valid sizing, or an edge.
- **Change made:** Six documentation files created. Application source, data, research and existing archive contents preserved.

## EXP-001 — initial crew audit (planned, not run)

- **Hypothesis:** The four-agent workflow can identify actionable, supported gaps with acceptable owner time and no additional paid-service use.
- **Prerequisites:** Verify included model and tool access; create a secret-free, project-scoped workspace; prevent broker side effects; agree a run budget.
- **Workflow:** Researcher reconciles requirements; engineer audits code; QA checks evidence and validation design; risk reviewer lists blockers.
- **Inputs:** This documentation baseline plus approved project files. Do not ingest credentials or the bundled environment.
- **Controls:** Manual sequential run, bounded iterations/retries/time, no paid fallback, no source edits for the audit.
- **Measure:** Actual elapsed time, owner intervention minutes, workflow executions consumed, token counts where available, recorded cost/charge evidence, supported findings, false findings, and next-task quality.
- **Comparison:** Later run a single-agent audit on the same file snapshot with a comparable task and usage budget. Record run order and any information leakage between comparisons.
- **Outputs:** Agent handoffs and one prioritised implementation task in `reports/`; record actual filenames after execution.
- **Status/results:** Not run. No model selected, account configured or quota consumed by this document.

## Template for subsequent experiments

### EXP-XXX — descriptive name

- **Date/time and timezone:**
- **Type / status:** Offline test, backtest, paper observation, etc.; planned/running/completed/failed/blocked.
- **Owner and participating agents:**
- **Hypothesis / change:** One defined question; link approved decision if needed.
- **Baseline and candidate:** Commit or file hashes; configuration and dependency versions.
- **Data:** Source, symbol identity, timezone, price basis, coverage, hashes and quality checks.
- **Evaluation split:** Chronological development, validation and untouched test windows; no shuffled future leakage.
- **Execution assumptions:** Entry timing, closed-bar availability, spread, commission, slippage, financing, latency, ambiguous intrabar handling.
- **Risk configuration:** Equity, account currency, per-trade and portfolio limits, RR and holding rules.
- **Commands / runner:** Exact reproducible command, working directory, environment and seed where relevant.
- **Acceptance criteria:** Prespecified checks and thresholds; identify unresolved criteria.
- **Actual results:** Counts, gross/net P&L, expectancy in R, drawdown, duration, exposure and breakdown by pair/period; mark unavailable metrics explicitly.
- **Uncertainty:** Sample size, dependence, sensitivity, limitations and alternative explanations.
- **Engineering / crew metrics:** Test outcomes, defects, elapsed time, owner time, calls/tokens, quota and monetary cost.
- **Artifacts:** Existing report/log paths and immutable run IDs; never invented filenames presented as completed evidence.
- **Verdict:** Supported, rejected, inconclusive or blocked, with reasoning.
- **Next action / approval:** Exact follow-up; proposal versus owner approval.

When revising a strategy, retain previous outcomes and all tried variants. Repeatedly inspecting the final holdout turns it into development data; obtain a new evaluation window before making further claims.
