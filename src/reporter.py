import json

def format_pr_comment(findings: list) -> str:
    """Convert findings list to a clean Markdown PR comment."""

    if not findings:
        return (
            "## CodeSentinel\n\n"
            "No security issues found.\n"
        )

    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for f in findings:
        counts[f.get('severity', 'Low')] += 1

    comment = "## CodeSentinel Security Review\n\n"
    comment += f"{len(findings)} issue(s) found\n\n"
    comment += "| Severity | Count |\n|----------|-------|\n"
    for sev, count in counts.items():
        if count > 0:
            comment += f"| {sev} | {count} |\n"

    comment += "\n"

    for f in findings:
        sev = f.get('severity', 'Low')
        vuln_type = f.get('type', 'Unknown')
        filename = f.get('file', 'unknown')
        line = f.get('line', 'N/A')
        description = f.get('description', '')
        fix = f.get('fix', '')

        comment += f"{sev}: {vuln_type} in `{filename}` (line {line})\n"
        comment += f"{description}\n"
        comment += f"Suggested fix: {fix}\n"
        comment += "\n"

    comment += (
        "Automated review by [CodeSentinel]"
        "(https://github.com/samuelHenris/CodeSentinel)\n"
    )
    return comment


def save_report(findings: list, output: str = "security-report.md"):
    """Save report to file and also a JSON summary."""
    with open(output, 'w') as f:
        f.write(format_pr_comment(findings))
    with open('findings.json', 'w') as f:
        json.dump(findings, f, indent=2)
    print(f"Report saved to {output} and findings.json")
