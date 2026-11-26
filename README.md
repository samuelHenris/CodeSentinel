# CodeSentinel: AI Security Reviewer for Pull Requests

A GitHub Action that reviews every pull request for common security problems before they are merged: OWASP Top 10 issues such as SQL injection and XSS, and hardcoded secrets such as API keys and passwords. It sends only the changed lines to a language model (the DeepSeek API) and posts the findings as a comment on the pull request.

I built it because security review often happens late, and a leaked key in a commit is expensive to clean up. Catching it at review time is cheap.

## How it works
1. A developer opens a Pull Request
2. CodeSentinel extracts the git diff (changed lines)
3. The diff is sent to DeepSeek's API with a security-review prompt
4. The model returns a JSON list of findings (severity, description, fix), which is parsed as data and never executed
5. The Action posts a structured report as a comment on the PR. It does not block the merge

## Features
- Detects OWASP Top 10 patterns (SQL injection, XSS, broken auth and more) and hardcoded secrets
- Scans only the lines changed in the PR, one request per file
- Runs in Docker, set up with one workflow file
- Each finding has a severity, the file and line, and a suggested fix

## First run (test scan on tests/sample_diff.txt)
- 9 API requests
- 2,634 tokens
- 3 vulnerabilities found (2 Critical, 1 High)
- Total cost: less than $0.01

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| AI Provider | DeepSeek `deepseek-chat` (OpenAI-compatible API) |
| Container | Docker |
| CI/CD | GitHub Actions |
| Diff Parsing | Custom pure-Python parser |
| Output | Markdown PR comment + JSON |

## Quick Start
1. Fork this repo
2. Add your `DEEPSEEK_API_KEY` to GitHub Secrets
3. The workflow (`.github/workflows/security-review.yml`) is already configured
4. Open a PR - CodeSentinel will automatically review it

## Example Output
```markdown
## CodeSentinel Security Review
**3 issue(s) found**

| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 1 |

### 1. SQL Injection
**File:** `app.py` line 4
**Fix:** Use parameterized queries...

### 2. Hardcoded Secret
**File:** `config.py` line 1
**Fix:** Move to environment variable...

## Limitations
- A language model can miss real vulnerabilities and flag harmless code. Treat the report as a first pass for a human reviewer, not a replacement for one.
- It only sees the changed lines, so it cannot judge how a change interacts with the rest of the codebase.
- Only some file types are scanned (see `scanner.py`).
- It does not fail the check when issues are found. It comments only.

## Privacy
Changed code is sent to the DeepSeek API to be analysed. Do not use this on repositories whose code you are not allowed to send to a third party. A self-hosted model would remove this limit.

## Tests
```bash
pip install openai pytest
python -m pytest tests
```
Tests cover the diff parser, the JSON handling of model replies (including a check that a malicious reply is never executed) and the report formatting.
