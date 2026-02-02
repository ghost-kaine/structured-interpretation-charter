#!/usr/bin/env python3
"""
Basic validator for the Minimal Machine Checklist:
- checks for required perspectives
- checks for 'Synthesis' section
- checks for labeled 'speculative'
- checks for resolution flag at the end (RESOLVED / PARTIALLY RESOLVED / REJECTED)
- checks for simple anthropomorphic terms (fail if present)
"""

import sys
import re
from pathlib import Path

def load_text(path):
    return Path(path).read_text(encoding='utf8')

def check_required_perspectives(text):
    required = ['Logical Evaluation', 'Constraint & Risk Assessment', 'Contextual / Factual Grounding']
    missing = [r for r in required if r not in text]
    return missing

def has_synthesis(text):
    return bool(re.search(r'(^|\n)##?\s*Synthesis', text, re.IGNORECASE))

def has_speculative_label(text):
    return 'speculative' in text.lower()

def has_resolution_flag(text):
    # Look near end for one of flags
    tail = text[-1000:]
    return bool(re.search(r'(RESOLVED|PARTIALLY RESOLVED|REJECTED)', tail))

def anthropomorphic_terms_found(text):
    terms = ['conscious', 'consciousness', 'intention', 'intent', 'feel', 'experience', 'selfhood', 'self']
    found = [t for t in terms if re.search(r'\b' + re.escape(t) + r'\b', text, re.IGNORECASE)]
    return found

def main(path):
    text = load_text(path)
    status = 0

    missing = check_required_perspectives(text)
    if missing:
        print(f"ERROR: missing required perspectives: {missing}")
        status = 2

    if not has_synthesis(text):
        print("ERROR: missing Synthesis section (header 'Synthesis' not found).")
        status = 2

    if not has_speculative_label(text):
        print("WARNING: no 'speculative' label found (recommended >=95% labeling).")

    if not has_resolution_flag(text):
        print("ERROR: resolution flag missing. Add RESOLVED / PARTIALLY RESOLVED / REJECTED at the end.")
        status = 2

    found = anthropomorphic_terms_found(text)
    if found:
        print(f"ERROR: anthropomorphic terms detected (disallowed): {found}")
        status = 2

    if status == 0:
        print("OK: CHARTER validation passed (basic checks).")
    else:
        print("FAILED: CHARTER validation did not pass basic checks.")

    sys.exit(status)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: validate_charter.py <path-to-markdown>")
        sys.exit(1)
    main(sys.argv[1])
