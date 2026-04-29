import json

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢"
}

def format_pr_comment(findings: list) -> str:
    """Convert findings list to a Markdown PR comment."""
    if not findings:
        return (
            "## CodeSentinel\n\n"
            " No security issues found.\n\n"
            "> Inspired by the recent Anthropic Claude source code leak. "
            "Don't let your secrets slip."
        )

    # Count severities
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for f in findings:
        counts[f.get('severity', 'Low')] += 1

    comment = "## CodeSentinel Security Review\n\n"
    comment += f"**{len(findings)} issue(s) found**\n\n"
    comment += "| Severity | Count |\n|----------|-------|\n"
    for sev, count in counts.items():
        if count > 0:
            comment += f"| {SEVERITY_EMOJI.get(sev, '⚪')} {sev} | {count} |\n"

    comment += "\n---\n"
    for i, f in enumerate(findings, 1):
        emoji = SEVERITY_EMOJI.get(f.get('severity', 'Low'), '⚪')
        comment += f"### {i}. {emoji} {f['type']}\n"
        comment += f"**File:** `{f.get('file','unknown')}` line {f.get('line','N/A')}\n\n"
        comment += f"**Description:** {f.get('description','')}\n\n"
        comment += f"**Fix:**\n```\n{f.get('fix','')}\n```\n\n---\n"

    comment += (
        "\n> 🤖 Automated review by [CodeSentinel]"
        "(https://github.com/samuelHenris/CodeSentinel) "
        ""
    )
    return comment

def save_report(findings: list, output: str = "security-report.md"):
    """Save report to file and also a JSON summary."""
    with open(output, 'w') as f:
        f.write(format_pr_comment(findings))
    with open('findings.json', 'w') as f:
        json.dump(findings, f, indent=2)
    print(f"Report saved to {output} and findings.json")

