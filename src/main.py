import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.diff_parser import parse_diff_by_file
from src.scanner import SecurityScanner
from src.reporter import format_pr_comment, save_report

def main():
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not set")
        sys.exit(1)

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            diff_text = f.read()
    elif not sys.stdin.isatty():
        diff_text = sys.stdin.read()
    else:
        print("Usage: python src/main.py diff.txt  OR  git diff | python src/main.py")
        sys.exit(1)

    if not diff_text.strip():
        print("No changes to scan.")
        return

    file_changes = parse_diff_by_file(diff_text)
    print(f"Changed files: {list(file_changes.keys())}")

    scanner = SecurityScanner(api_key)
    findings = scanner.scan_changes(file_changes)

    print(f"Found {len(findings)} issue(s).")
    report = format_pr_comment(findings)
    save_report(findings)
    print(report)

if __name__ == "__main__":
    main()
