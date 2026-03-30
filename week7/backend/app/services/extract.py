import re


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text using pattern recognition.
    
    Matches patterns like:
    - Lines starting with TODO:, ACTION:, or TASK: (case-insensitive)
    - Lines starting with Markdown checkboxes [ ], [x], or [X]
    - Lines ending with an exclamation mark !
    """
    lines = [line.strip("- *").strip() for line in text.splitlines() if line.strip()]
    results: list[str] = []
    
    # Regex patterns
    keyword_pattern = re.compile(r'^(todo|action|task):', re.IGNORECASE)
    checkbox_pattern = re.compile(r'^\[\s*[xX]?\s*\]')
    
    for line in lines:
        # Match keyword patterns (TODO:, ACTION:, TASK:)
        if keyword_pattern.match(line):
            results.append(line)
        # Match Markdown checkboxes [ ], [x], [X]
        elif checkbox_pattern.match(line):
            results.append(line)
        # Match lines ending with exclamation mark
        elif line.endswith("!"):
            results.append(line)
    
    return results


