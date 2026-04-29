# CodeSentinel - AI-Powered Security Code Reviewer

**"Because code leaks happen."**

After Anthropic accidentally published the Claude model's source code on GitHub, one question remained: **How do we catch secrets and vulnerabilities before they're merged?** CodeSentinel is the answer.

A GitHub Action that automatically scans every pull request for OWASP Top 10 vulnerabilities, hardcoded secrets, and insecure patterns - using **DeepSeek's V4 Flash model**, which matches and beats Claude on coding benchmarks, at a fraction of the cost.

## How it works
1. A developer opens a Pull Request
2. CodeSentinel extracts the git diff (changed lines)
3. The diff is sent to DeepSeek's API with a security-review prompt
4. The AI returns a JSON list of findings (severity, description, fix)
5. The Action posts a structured report directly on the PR

## Features
- OWASP Top 10 detection - SQLi, XSS, CSRF, broken auth, and more
- Hardcoded secret scanning - API keys, tokens, passwords
- Powered by DeepSeek V4 Flash - the newest model, matching/exceeding Claude on code understanding
- Containerised with Docker - runs consistently anywhere
- GitHub Action - one YAML file, zero infrastructure to maintain
- Actionable fixes - every issue comes with a code suggestion

## First Run Stats (test scan)
- 9 API requests
- 2,634 tokens
- 3 vulnerabilities found (2 Critical, 1 High)
- Total cost: less than $0.01

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| AI Provider | DeepSeek (OpenAI-compatible API) |
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
