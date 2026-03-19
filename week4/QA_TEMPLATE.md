# QA Automation Prompt for Copilot Chat
When the user types "Run QA Pipeline", execute the following workflow using the `@workspace` and `/terminal` context:
1. Analyze the workspace for any recent changes.
2. Suggest the terminal commands: `make format`, then `make lint`, then `make test`.
3. If the user pastes an error log from the terminal, automatically analyze the traceback, pinpoint the exact file, and generate the fix.