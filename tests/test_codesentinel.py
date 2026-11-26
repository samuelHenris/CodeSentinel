import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.diff_parser import parse_diff_by_file
from src.reporter import format_pr_comment
from src.scanner import SecurityScanner

SAMPLE = os.path.join(os.path.dirname(__file__), "sample_diff.txt")


def make_scanner():
    return SecurityScanner("test-key")


def test_diff_parser_groups_by_file_with_line_numbers():
    with open(SAMPLE) as f:
        files = parse_diff_by_file(f.read())
    assert set(files) == {"app.py", "config.py", "utils.js"}
    assert files["config.py"][0]["line"] == 1
    assert "sk-proj" in files["config.py"][0]["code"]


def test_diff_parser_keeps_directory_names_containing_a():
    diff = (
        "diff --git a/src/data/x.py b/src/data/x.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+password = 'abc'\n"
    )
    assert list(parse_diff_by_file(diff)) == ["src/data/x.py"]


def test_parse_response_reads_fenced_json():
    reply = '```json\n[{"severity": "High", "type": "SQLi", "line": 4}]\n```'
    assert make_scanner()._parse_response(reply)[0]["type"] == "SQLi"


def test_parse_response_never_executes_code():
    marker = "/tmp/codesentinel_eval_test"
    if os.path.exists(marker):
        os.remove(marker)
    evil = "__import__('os').system('touch %s')" % marker
    assert make_scanner()._parse_response(evil) == []
    assert not os.path.exists(marker)


def test_parse_response_handles_bad_output():
    s = make_scanner()
    assert s._parse_response("not json") == []
    assert s._parse_response('{"a": 1}') == []
    assert s._parse_response("") == []


def test_report_handles_unexpected_severity():
    out = format_pr_comment([{"severity": "critical", "type": "X", "file": "a.py", "line": 1}])
    assert "Critical" in out
    out = format_pr_comment([{"severity": "Info", "type": "X", "file": "a.py", "line": 1}])
    assert "1 issue(s) found" in out


def test_report_when_clean():
    assert "No security issues" in format_pr_comment([])
