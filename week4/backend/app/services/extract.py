import re

def extract_action_items(text: str) -> list[str]:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    items = []
    for line in lines:
        if "ignore" in line.lower():
            continue
        if line.endswith("!") or line.lower().startswith("todo:") or re.search(r"#\w+", line):
            items.append(line)
    return items
