# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **CLARISSA DHEA ALLISYA** \
SUNet ID: **2410817220023** \
Citations: **Warp AI Agent, Claude Haiku 4.5 (via Cursor)**

This assignment took me about **4** hours to do. 

## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Automate the implementation of regex-based parsing for `#hashtags` and `-[ ] action items` in `extract.py` (Task 6), including endpoint creation and database persistence.
> **Inputs/Outputs:** Provided a structured Warp Drive Saved Prompt instructing the agent to analyze `extract.py`, write regex patterns, add a `POST /notes/{id}/extract` route, and implement tests. The output is the modified codebase successfully passing all 23 tests.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Manual:** Searching for correct regex syntax, manually wiring up FastAPI endpoints, writing boilerplate database persistence logic, and debugging test failures iteratively.
> **Automated:** The Warp agent executed the full pipeline autonomously. It read the prompt, wrote the business logic, formatted the code using `black`/`ruff`, and self-corrected during `pytest` until all tests passed.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> **High Autonomy.** The agent was given read/write permissions to the codebase and permission to execute tests/linters. Supervision was done via standard Warp permission prompts (Approve/Deny) for terminal execution to ensure it didn't run malicious commands.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A for this specific automation.

e. How you used the automation (what pain point it resolves or accelerates)
> It significantly accelerates the boilerplate phase of endpoint creation and the tedious trial-and-error often associated with regex parsing and test-driven development.


### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Implement two separate API features simultaneously using multiple AI agents without code clobbering. Agent 1 implemented the Notes search API with pagination and sorting (Task 2). Agent 2 implemented List endpoint pagination for all collections (Task 8).
> **Inputs/Outputs:** Two separate prompts deployed concurrently in two different Warp tabs targeting different Git branches. The output was two fully functional, tested features.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Manual:** A linear workflow where Task 2 must be completed, tested, and committed before starting Task 8 to avoid confusion.
> **Automated:** Parallel feature delivery where both tasks are developed, linted, and tested simultaneously by different agents.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> **High Autonomy.** Both agents handled their respective test-driven development loops autonomously, requiring supervision only to approve terminal commands. 

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Coordination Strategy:** Used `git worktree` to create a completely isolated working directory (`week5-task2`) linked to the same repository. This allowed Agent 1 to work on the `master` branch while Agent 2 worked concurrently on the `task-2-search` branch.
> **Wins/Risks:** Drastically reduced implementation time. Both agents completed complex SQLAlchemy queries and passed over 30 combined tests in parallel. The risk was encountering merge conflicts in shared files like `routers.py` and `schemas.py`, which we did experience and successfully resolved manually using our editor's merge tool.

e. How you used the automation (what pain point it resolves or accelerates)
> Eliminates the linear bottleneck of solo development. By delegating isolated tasks to separate agents, feature delivery time is effectively cut in half, proving the viability of scalable, concurrent agentic workflows.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> N/A

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> N/A

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A

e. How you used the automation (what pain point it resolves or accelerates)
> N/A