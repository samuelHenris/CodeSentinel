"""Parse git diff for changed code lines."""

def parse_diff(diff_text: str) -> list:
    changes = []
    current_file = ""
    current_line = 0
    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            current_file = line.split(' ')[2].replace('a/', '')
        elif line.startswith('@@'):
            parts = line.split(' ')
            if len(parts) >= 3:
                new_info = parts[2]
                if new_info.startswith('+'):
                    current_line = int(new_info.split(',')[0].replace('+', ''))
                else:
                    current_line = int(new_info)
        elif line.startswith('+') and not line.startswith('+++'):
            changes.append({
                'file': current_file,
                'line': current_line,
                'code': line[1:].strip()
            })
            current_line += 1
        elif not line.startswith('-') and not line.startswith('---'):
            current_line += 1
    return changes

def parse_diff_by_file(diff_text: str) -> dict:
    """Group changes by file."""
    all_changes = parse_diff(diff_text)
    by_file = {}
    for change in all_changes:
        filename = change['file']
        if filename not in by_file:
            by_file[filename] = []
        by_file[filename].append(change)
    return by_file
