import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a senior security engineer conducting a code review.
Look for:
- OWASP Top 10 vulnerabilities (SQL injection, XSS, etc.)
- Hardcoded secrets (API keys, passwords, tokens)
- Sensitive data exposure (internal URLs, proprietary algorithms)
- Insecure configurations

Respond ONLY with a JSON array of findings (no extra text). Each finding must have:
{
  "severity": "Critical|High|Medium|Low",
  "type": "vulnerability type",
  "file": "filename",
  "line": line_number,
  "description": "what's wrong",
  "fix": "code fix suggestion"
}
If no issues, return [].
"""

class SecurityScanner:
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = model

    def scan_changes(self, file_changes: dict) -> list:
        all_findings = []
        for filename, changes in file_changes.items():
            if not filename.endswith(
                ('.py','.js','.java','.ts','.go','.rb','.php','.yaml','.yml','.json','.tf')
            ):
                continue

            code_block = f"File: {filename}\n"
            for c in changes:
                code_block += f"Line {c['line']}: {c['code']}\n"

            print(f"Scanning {filename} ({len(changes)} lines)...")

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": code_block}
                    ],
                    temperature=0.1
                )
                findings = self._parse_response(response.choices[0].message.content)
                for f in findings:
                    f['file'] = filename
                all_findings.extend(findings)
            except Exception as e:
                print(f"Error scanning {filename}: {e}")

        return all_findings

    def _parse_response(self, content: str) -> list:
        if content.startswith('```json'):
            content = content[7:-3]
        elif content.startswith('```'):
            content = content[3:-3]
        try:
            return eval(content)  # Use json.loads in production
        except:
            return []
