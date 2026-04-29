## CodeSentinel Security Review

3 issue(s) found

| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 1 |

Critical: SQL Injection in `app.py` (line 4)
User input is directly concatenated into SQL query without sanitization, allowing SQL injection attacks.
Suggested fix: Use parameterized queries: query = 'SELECT * FROM users WHERE id = ?'; cursor.execute(query, (user_id,))

Critical: Hardcoded Secret in `config.py` (line 1)
Hardcoded OpenAI API key exposes sensitive credentials, allowing unauthorized access to OpenAI services and potential financial abuse.
Suggested fix: Remove the hardcoded key and use environment variables: OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

High: Cross-Site Scripting (XSS) in `utils.js` (line 1)
User input from req.body.name is directly assigned to a variable without sanitization or encoding, which can lead to stored or reflected XSS if this value is later rendered in HTML or executed as code.
Suggested fix: Sanitize the input using a library like DOMPurify or encode output with context-appropriate escaping (e.g., encodeURIComponent for URLs, escapeHtml for HTML). Example: var userInput = DOMPurify.sanitize(req.body.name);

Automated review by [CodeSentinel](https://github.com/samuelHenris/CodeSentinel)
