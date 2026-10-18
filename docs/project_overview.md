# Project Mayhem — project overview

Updated: 18 October 2026. Version: 0.1. Status: initial documentation baseline.

Paths in this document are relative to the project root unless a Markdown link is used.

## Purpose and current scope

Project Mayhem is Evan Harrington's existing Python automated foreign-exchange trading project. Its current development brief targets GBPJPY and USDJPY, using hourly areas of interest and 15-minute confirmation. The business objective is to investigate positive performance after realistic costs while producing reliable, testable software. Daily profit is an aspiration, not an acceptance criterion that agents can guarantee.

The uploaded project is a prototype for MT5 data collection and rule-based pattern analysis. It is not a verified trading system. No broker session, live order, paper trade, or profitability test was performed while preparing these documents.

Read next: [strategy specification](strategy_specification.md), [risk policy](risk_policy.md), [data dictionary](data_dictionary.md), [decision log](decision_log.md), and [experiment log](experiment_log.md).

## Evidence and precedence

1. The current owner brief in this conversation establishes the target pairs, H1/M15 sequence, initial 2R target, intended maximum 2% per-trade risk, and short-duration objective.
2. `docs/Strategy.txt` is historical planning material. Its Phase 1 plan selects the MetaTrader5 API; its Phase 2 plan lists candidate checks and possible libraries. Examples such as RSI and engulfing candles are not approved strategy requirements.
3. Existing source code establishes implemented behaviour, not necessarily intended or correct behaviour.
4. Research files provide historical context. New interpretations must be recorded as proposals until the owner resolves them.

The earlier assistant recommended controlled releases and independent validation. These are the proposed development operating baseline, not evidence that the owner has approved every suggested trading parameter. See the decision log for status distinctions.

## Repository map

| Location | Observed contents | Agent use |
|---|---|---|
| `docs/Strategy.txt` | Broker, data, automation, testing, and optional ML roadmap | Historical rationale |
| `docs/Automatic Trading Software.pages` | Historical architecture and strategy notes | Export to readable text/PDF before full ingestion |
| `src/ProjectMayhem/` | Six Python modules and seven CSV snapshots | Actual implementation and fixture evidence |
| `research/` | Chart screenshots, Pages notes, a trading psychology PDF, and `Phase2Map.png` | Context; not a substitute for reproducible results |
| `tests/` | No supplied test files | Future independent tests |
| `skills/` | No supplied skill files | Future working procedures; not configured by this update |
| `reports/` | No supplied report files | Future execution evidence |

The uploaded archive also contains a bundled virtual environment and IDE metadata. They are retained in this documentation-only update. Do not ingest the environment into the agent knowledge base or treat it as a reproducible dependency manifest.

## Implementation map

| Module | Implemented responsibility | Important limitation |
|---|---|---|
| `main.py` | MT5 calls, M1/M15/H1 collection, CSV writing, threaded scheduler | Hard-coded GBPJPY; account login at import; strategy schedule commented out |
| `OrderBlockAnalysis.py` | Candidate OB creation and validation for M15/H1 | Reads later candles; historical signal availability must be reconstructed |
| `FairValueGap.py` | M15 three-candle FVG detection and later invalidation scan | No H1 FVG pipeline; fixed file and price thresholds |
| `Liquidity.py` | M15 wick/price-level heuristic and later validation | Fixed thresholds differ materially across branches; rule intent unverified |
| `Strategy.py` | Session, OB overlap, direction and FVG checks | Incomplete state handling and entry sequence |
| `Execution.py` | Experimental size calculation and execution stubs | `taketrade()` prints “Work in progress”; `main()` returns without placing an order |

## Entry point and dependencies

The historical entry point is `src/ProjectMayhem/main.py`, with file paths resolved from the process working directory. This is not a recommendation to run it now: importing it already calls `mt.login`, and running it starts broker-connected collection and a long-running scheduler.

Direct external imports are `MetaTrader5`, `pandas`, `pytz`, and `tzlocal`; other imports are Python standard library or sibling modules. No project-owned `requirements.txt`, lockfile, or `pyproject.toml` was found outside the bundled environment. `OrderBlockAnalysis.py` uses the `int | None` annotation, so Python 3.10+ is the inferred source-language starting point; package and platform compatibility are not verified. The MT5 terminal, broker configuration, and supported execution host remain prerequisites for broker-connected work.

Before agents execute application code, create an isolated offline harness, remove broker side effects from imports in a reviewed change, and establish a dependency manifest. Do not blindly copy packages out of the bundled environment.

## Static findings to reproduce

| ID | Evidence | Consequence / next investigation |
|---|---|---|
| F01 | `main.py`, module-level authentication assignments and `mt.login` | Embedded account credentials and broker side effects; externalise credentials before connecting agents |
| F02 | `main.py`, `symbol` and CSV writers | GBPJPY selected but GBPUSD filenames used; USDJPY has no independent stream |
| F03 | `main.py::write_15m` | Append branch selects `data.iloc[-1]` (a Series) then calls `.iterrows()`; expected append failure, not runtime-tested here |
| F04 | `Strategy.py::check_if_in_ob_hr` | `NoOfCandles += 1` has no assignment in that module; a matching OB can raise `NameError` |
| F05 | `Strategy.py::correct_dir` and `check_if_in_fvg` | OB row index reused to index a current-candle file that contains one row; confirmation state/history cannot be assumed valid |
| F06 | `main.py::schedules` and `main()` | Normal strategy scheduling is commented out; trailing strategy call occurs after scheduler exit and MT5 shutdown |
| F07 | Detector validation functions | Later data affects whether earlier zones remain in output; unsuitable as historical entry evidence without event-time reconstruction |
| F08 | `OrderBlockAnalysis.py::Analyse_Data` | Loop starts at zero and uses `df.iloc[i-1]`; the first iteration can reference the last row |
| F09 | `main.py`, candle retrieval/writers | Requests include position zero; candle completion is not established; exported timezone is stripped |
| F10 | `Execution.py` and empty `tests/` | No executable trade lifecycle, independent tests, or measured performance baseline |

These are code-inspection findings, not a full defect audit. Scheduler overlap, atomic CSV updates, error recovery, signal direction, and broker specification handling also require review.

## Team and initial work order

| Owner | First deliverable |
|---|---|
| Strategy Researcher | Reconcile source documents and unresolved rules into timestamp-aware acceptance criteria |
| Senior Engineer | Reproduce prototype defects offline and propose the smallest coherent repair |
| QA / Backtesting Engineer | Build independent fixture checks; identify realistic backtest requirements |
| Risk / Execution Reviewer | Verify deterministic controls and list release blockers |
| Product owner | Resolve strategy ambiguities, approve material changes, and control release authority |

Start with a sequential, manual, read-only audit. Give agents only project-scoped access. Documentation is not an access-control mechanism. No CrewAI account settings, tools, MCP connections, paid services, or agents were configured by adding these files.

## Research coverage

The six source modules, all seven CSV files, and `Strategy.txt` were inspected. `research/Phase2Map.png` was visually inspected: it lists candidate libraries, not installed requirements. Only the embedded first-page preview of `Automatic Trading Software.pages` was inspected; it mentions a modular Python design, session liquidity, structural breaks, and a 50% supply-box area. Its session wording is historical and does not resolve current trading-session decisions.

The remaining Pages documents, screenshot collection, and full PDF were inventoried but not fully interpreted. Agents must not claim these materials have already been reconciled. Export Pages documents to searchable PDF or text and inspect chart timestamps and annotations before using them as requirements. Preserve the originals.
